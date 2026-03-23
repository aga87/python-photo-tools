from pathlib import Path


def organise_by_date(input_dir: str, output_dir: str) -> None:
    input_path = Path(input_dir)
    output_path = Path(output_dir)

    if not input_path.exists():
        raise FileNotFoundError(f"Folder {input_path} does not exist")
    

    if not input_path.is_dir():
        raise NotADirectoryError(f"Expected a folder but got: {input_path}")

    # TODO: implement
    print(f"Organising from {input_path} → {output_path}")