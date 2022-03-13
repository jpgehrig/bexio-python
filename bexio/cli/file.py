import click

from pathlib import Path
from dateutil import parser

from ..api import APIClient
from . import pass_config


@click.group()
def file():
    """
    Manage files.
    """
    pass

@file.command()
@click.option('-s', '--archived_state',
              required=True,
              type=click.Choice(['all', 'archived', 'not_archived']),
              help='The `archived_state` of the files to download.')
@click.option('-d', '--directory',
              required=True,
              type=click.Path(exists=True, file_okay=False, path_type=Path),
              help='The directory to save files.')
@click.option('-p', '--prefix',
              type=click.Choice(['date']),
              help='Prefix to apply to download files.')
@pass_config
def download_all(config, archived_state, directory, prefix):
    """
    Download all files.
    """
    client = APIClient()
    params = {
        'archived_state': archived_state,
        'offset': 0,
        'limit': 100
    }
    response = client.get('3.0/files', params=params)
    count = int(response.headers['X-Total-Count'])
    with click.progressbar(length=count, label=f'Downloading {count} files') as bar:
        while response.json():
            for i, f in enumerate(response.json()):
                created_at = parser.parse(f['created_at'])
                date = created_at.strftime('%Y%m%d')
                filename = f"{f['name']}.{f['extension']}"
                if prefix == 'date':
                    filename = f'{date}_{filename}'
                r = client.get(f"3.0/files/{f['id']}/download")
                filepath = directory / filename
                with filepath.open('wb') as f:
                    f.write(r.content)
                bar.update(1)
            params['offset'] += len(response.json())
            response = client.get('3.0/files', params=params)
