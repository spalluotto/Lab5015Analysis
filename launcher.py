from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import subprocess

cfg_dir = Path("cfg")
bin_dir = Path("bin")
setup_script = "scripts/setup.sh"
MAXJOBS = 8

cfg_files = [
    "moduleCharacterization_DM_FE_4587_Vov3.00_T18C_positionScan_PDEGaincor_refBar6_TOFHIRcalib.cfg",
    "moduleCharacterization_DM_FE_4587_Vov3.00_T18C_positionScan_PDEGaincor_refBar7_TOFHIRcalib.cfg",
    "moduleCharacterization_DM_FE_4587_Vov3.00_T18C_positionScan_PDEGaincor_refBar8_TOFHIRcalib.cfg",
    "moduleCharacterization_DM_FE_4587_Vov3.00_T18C_positionScan_PDEGaincor_refBar9_TOFHIRcalib.cfg",
    "moduleCharacterization_DM_FE_4587_Vov3.00_T18C_positionScan_PDEGaincor_refBar10_TOFHIRcalib.cfg",
]
cfg_files = [cfg_dir / f for f in cfg_files]

def run_job(cfg_path: Path):
    try:
        print(f"=== STEP1: {cfg_path.name} ===")
        subprocess.run(f"source {setup_script} && {bin_dir}/moduleCharacterization_step1.exe {cfg_path}", shell=True, executable="/bin/bash", check=True)
        print(f"=== STEP2: {cfg_path.name} ===")
        subprocess.run(f"source {setup_script} && {bin_dir}/moduleCharacterization_step2.exe {cfg_path}", shell=True, executable="/bin/bash", check=True)
        print(f"=== DONE: {cfg_path.name} ===")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] su {cfg_path.name}: {e}")

with ThreadPoolExecutor(max_workers=MAXJOBS) as executor:
    list(executor.map(run_job, cfg_files))
