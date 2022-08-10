use std::{
    collections::{HashMap, HashSet},
    fs::{create_dir, File},
    io::Write,
};

use bgpkit_parser::BgpkitParser;
use chrono::prelude::*;
use clap::Parser;
use ipnetwork::{IpNetwork, Ipv4Network};

#[derive(Parser, Debug)]
struct Opt {
    #[clap(long, help = "Route collector no.", default_value = "00")]
    rrc: String,

    #[clap(long, name = "YYYY-MM-DD")]
    date: Option<String>,

    #[clap(long, name = "hh:MM", default_value = "00:00")]
    time: String,

    #[clap(long, help = "Filter for supernets of a prefix.")]
    prefix: Option<String>,

    #[clap(long, short = 'a', help = "Write ASN -> prefixes mapping file.")]
    asn_prefix_mapping: bool,

    #[clap(long, short = 'p', help = "Write prefix -> ASN mapping file.")]
    prefix_asn_mapping: bool,
}

fn write_prefix_mapping_files(
    prefix_asn: &mut HashMap<String, HashSet<String>>,
    prefix_asn_file: &mut File,
) -> std::io::Result<()> {
    for (prefix, asns) in prefix_asn.drain() {
        let mut line = prefix + " |";
        for asn in asns {
            line += " ";
            line += &asn;
        }
        line += "\n";
        prefix_asn_file.write(line.as_bytes())?;
    }
    Ok(())
}

fn write_asn_mapping_files(
    asn_prefix: &mut HashMap<String, Vec<String>>,
    asn_prefix_file: &mut File,
) -> std::io::Result<()> {
    for (asn, prefixes) in asn_prefix.drain() {
        let mut line = asn + " |";
        for prefix in prefixes {
            line += " ";
            line += &prefix;
        }
        line += "\n";
        asn_prefix_file.write(line.as_bytes())?;
    }
    Ok(())
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let opt = Opt::parse();
    let (hour, minute) = {
        let parts: Vec<_> = opt.time.split(":").map(ToString::to_string).collect();
        if parts.len() != 2 {
            return Err("Invalid time format. Please enter the time in the format hh:MM.".into());
        }
        (parts[0].clone(), parts[1].clone())
    };
    let (year, month, day) = match opt.date {
        Some(data_string) => {
            let parts: Vec<_> = data_string.split("-").map(ToString::to_string).collect();
            if parts.len() != 3 {
                return Err(
                    "Invalid date format. Please enter the date in the format YYYY-MM-DD.".into(),
                );
            }
            (parts[0].clone(), parts[1].clone(), parts[2].clone())
        }
        None => {
            let date: DateTime<Local> = Local::now();
            (
                date.format("%Y").to_string(),
                date.format("%m").to_string(),
                date.format("%d").to_string(),
            )
        }
    };
    let file_name = format!("bview.{0}{1}{2}.{3}{4}.gz", year, month, day, hour, minute);
    let url = format!(
        "https://data.ris.ripe.net/rrc{0}/{1}.{2}/{3}",
        opt.rrc, year, month, file_name
    );
    let contain_prefix: Option<Ipv4Network> = match opt.prefix {
        Some(prefix) => Some(prefix.parse()?),
        None => None,
    };

    let _ = create_dir("../data");
    let mut prefix_asn_mapping_file = opt.prefix_asn_mapping.then(|| File::create("../data/prefix_asn_mapping.csv").unwrap());
    let mut asn_prefix_mapping_file = opt.asn_prefix_mapping.then(|| File::create("../data/asn_prefix_mapping.csv").unwrap());
    let mut prefix_asn: HashMap<_, HashSet<_>> = HashMap::new();
    let mut asn_prefix: HashMap<_, Vec<_>> = HashMap::new();

    let mut current_first_octet = 0;
    let parser = BgpkitParser::new(&url).unwrap();
    parser
        .into_iter()
        .filter(|elem| {
            let ipv4network = match elem.prefix.prefix {
                IpNetwork::V4(prefix) if prefix.prefix() != 0 => prefix,
                _ => return false,
            };

            match contain_prefix {
                Some(p) => ipv4network.is_supernet_of(p),
                None => true,
            }
        })
        .try_for_each::<_, Result<(), std::io::Error>>(|elem| {
            let first_octet = match elem.prefix.prefix {
                IpNetwork::V4(prefix) => prefix.ip().octets()[0],
                IpNetwork::V6(_) => unreachable!(),
            };
            if first_octet != current_first_octet {
                if let Some(file) = prefix_asn_mapping_file.as_mut() {
                    write_prefix_mapping_files(&mut prefix_asn, file)?;
                }
                if let Some(file) = asn_prefix_mapping_file.as_mut() {
                    write_asn_mapping_files(&mut asn_prefix, file)?;
                }
                current_first_octet = first_octet;
            }
            if let Some(asn) = elem
                .as_path
                .and_then(|path| path.to_string().split(" ").last().map(|s| s.to_string()))
            {
                let entry = prefix_asn.entry(elem.prefix.to_string()).or_default();
                if entry.insert(asn.clone()) {
                    println!("Prefix: {}| ASN: {}", elem.prefix.to_string(), asn);
                    asn_prefix
                        .entry(asn)
                        .or_default()
                        .push(elem.prefix.to_string());
                }
            }
            Ok(())
        })?;
    Ok(())
}
