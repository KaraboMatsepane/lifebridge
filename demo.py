from pathlib import Path

private_key = Path("keys/public.pem").read_text()



if __name__ == "__main__":
    print(private_key)