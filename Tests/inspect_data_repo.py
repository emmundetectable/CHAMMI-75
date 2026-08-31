"""Browse the public CHAMMI S3 bucket structure (no AWS credentials needed)."""

import boto3
from botocore import UNSIGNED
from botocore.config import Config

BUCKET = "chammi-data"
# Change this to drill into a folder, e.g. "CHAMMI-75/" or "CHAMMI-75/CHAMMI-75_test/"
PREFIX = ""
MAX_KEYS = 50  # how many objects/prefixes to print per listing


def list_level(s3, prefix: str, max_keys: int = MAX_KEYS):
    """List immediate children under prefix (like `aws s3 ls s3://bucket/prefix`)."""
    paginator = s3.get_paginator("list_objects_v2")
    pages = paginator.paginate(Bucket=BUCKET, Prefix=prefix, Delimiter="/")

    folders, files = [], []
    for page in pages:
        folders.extend(p["Prefix"] for p in page.get("CommonPrefixes", []))
        files.extend(o["Key"] for o in page.get("Contents", []) if o["Key"] != prefix)
        if len(folders) + len(files) >= max_keys:
            break

    print(f"\n=== s3://{BUCKET}/{prefix} ===")
    print(f"folders ({len(folders)} shown):")
    for f in folders[:max_keys]:
        print(f"  {f}")
    print(f"files ({len(files)} shown):")
    for f in files[:max_keys]:
        print(f"  {f}")


def main():
    s3 = boto3.client("s3", config=Config(signature_version=UNSIGNED))

    # 1) top level of the bucket
    list_level(s3, PREFIX)

    # 2) one level deeper into CHAMMI-75/ (comment out if not present)
    list_level(s3, "CHAMMI-75/")

    # 3) peek at the test set (where Jump-CP may live)
    list_level(s3, "CHAMMI-75/CHAMMI-75_test/")


if __name__ == "__main__":
    main()