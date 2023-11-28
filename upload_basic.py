import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload


def upload_basic(creds, saved_filename):
  """Insert new file.
  Returns : Id's of the file uploaded

  Load pre-authorized user credentials from the environment.
  TODO(developer) - See https://developers.google.com/identity
  for guides on implementing OAuth2 for the application.
  creds, _ = google.auth.default()
  """

  try:
    # create drive api client
    service = build("drive", "v3", credentials=creds)

    file_metadata = {"name": saved_filename}
    media = MediaFileUpload(saved_filename, mimetype="image/png")
    # pylint: disable=maybe-no-member
    file = (
        service.files()
        .create(body=file_metadata, media_body=media, fields="id", supportsAllDrives=True)
        .execute()
    )
    print(f'File ID: {file.get("id")}')

    anyone_permission = {
      'type': 'anyone'
    }
    service.permissions().create(
        fileId=file.get("id"),
        body=anyone_permission
    ).execute()

  except HttpError as error:
    print(f"An error occurred: {error}")
    file = None

  return file.get("id")


if __name__ == "__main__":
  upload_basic()
