import os
import shutil
import subprocess
import tempfile
import boto3
from botocore.exceptions import NoCredentialsError

# Configuration
bitbucket_repo_url = 'https://kabiranwar:Mybitbucketpwd@bitbucket.org/kabiranwar/newbitbucketproj.git'
bitbucket_username = 'kabiranwar'
bitbucket_app_password = 'aaaaa'
bitbucket_repo_url = f'https://{bitbucket_username}:{bitbucket_app_password}@bitbucket.org/kabiranwar/newbitbucketproj.git'



s3_bucket_name = 'baby1220'
s3_object_name = 'latest_master-apr3_2.zip'
commit_id = 'd68f576'  # Replace with the specific commit ID you want to clone


# Clone the Bitbucket repository
def clone_repo(repo_url, clone_path):
    if os.path.exists(clone_path):
        shutil.rmtree(clone_path)
    subprocess.run(['git', 'clone', repo_url, clone_path], check=True)

# Checkout the specific commit
def checkout_commit(repo_path, commit):
    subprocess.run(['git', 'checkout', commit], cwd=repo_path, check=True)

# Zip the cloned repository
def zip_repo(source_path, zip_path):
    shutil.make_archive(zip_path.replace('.zip', ''), 'zip', source_path)

# Upload the zip file to S3
def upload_to_s3(file_path, bucket, object_name):
    s3_client = boto3.client('s3')
    try:
        s3_client.upload_file(file_path, bucket, object_name)
        print(f"Upload Successful: {object_name}")
    except FileNotFoundError:
        print("The file was not found")
    except NoCredentialsError:
        print("Credentials not available")

# Main function
def main():
    with tempfile.TemporaryDirectory() as temp_dir:
        repo_dir = os.path.join(temp_dir, 'repo')
        zip_path = os.path.join(temp_dir, 'latest_master')
        clone_repo(bitbucket_repo_url, repo_dir)
        checkout_commit(repo_dir, commit_id)
        zip_repo(repo_dir, zip_path)
        upload_to_s3(f"{zip_path}.zip", s3_bucket_name, s3_object_name)

if __name__ == "__main__":
    main()
