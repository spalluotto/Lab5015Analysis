import subprocess

# --- TB configs ---
configs = {
    "config_82.00": {
        "module": "DM_9000",
        "vov_runs": {2: [4143], 3: [4140]},
        "do_refBar": True,
        "do_tof_calib": True,
        "do_tofLO_calib": True
    },
    "config_85.00": {
        "module": "DM_9005",
        "vov_runs": {2: [4235, 4236], 3: [4231, 4232]},
        "do_refBar": True,
        "do_tof_calib": True,
        "do_tofLO_calib": True
    },
    "config_87.00": {
        "module": "DM_9001",
        "vov_runs": {0.9: [4265], 1.2: [4259], 2: [4258], 3: [4257]},
        "do_refBar": True,
        "do_tof_calib": True,
        "do_tofLO_calib": True
    }
}
refBars = list(range(16))

# --- Generate commands ---
for cfg, info in configs.items():
    module = info["module"]
    do_refBar = info.get("do_refBar", False)

    # Build whichEnergy list according to config flags
    whichEnergy = [None]
    if info.get("do_tof_calib", False):
        whichEnergy.append("TOFHIR")
    if info.get("do_tofLO_calib", False):
        whichEnergy.append("TOFHIR_LO")

    for ov, runs in info["vov_runs"].items():
        for run in runs:
            for we in whichEnergy:
                # Base command
                args = f"-t 18 -ml {module} -c {cfg} -ov {ov} -r {run} -th vth1"
                if we:
                    args += f" --whichEnergyIntercalib {we}"
                #print(f"python3 create_config.py {args}")
                subprocess.run(["python3", "create_config.py"] + args.split(), check=True)
                
                # Optional refBar loop
                if do_refBar:
                    for i in refBars:
                        args_bar = args + f" --refBar {i}"
                        subprocess.run(["python3", "create_config.py"] + args_bar.split(), check=True)
                        #print(f"python3 create_config.py {args_bar}")
                        
