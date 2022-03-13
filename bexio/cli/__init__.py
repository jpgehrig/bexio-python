import click
import bexio
import os

from .config import pass_config

from .file import file


class CatchBexioAPIError(click.Group):

    def __call__(self, *args, **kwargs):
        try:
            return self.main(*args, **kwargs)
        except bexio.exceptions.BexioAPIError as e:
            click.secho(f'\n! API ERROR: {e} [{e.status_code}]', bold=True, fg='red')
            click.secho(f'!  endpoint: {e.url}\n', fg='red')


@click.group(cls=CatchBexioAPIError)
@click.option('--api-token', envvar='BEXIO_API_TOKEN', required=True)
@click.option('--api-host', envvar='BEXIO_API_HOST', default='https://api.bexio.com')
@click.option('--verbose', is_flag=True)
@pass_config
def main(config, api_token, api_host, verbose):
    config.verbose = verbose
    bexio.config.api_token = api_token
    bexio.config.api_host = api_host


main.add_command(file)
