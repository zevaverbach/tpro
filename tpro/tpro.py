import json

import click

from .converters import services
from . import outputs
from . import helpers

output_choices =  [k for k, v in 
                   outputs.__dict__.items()
                   if callable(v)]

@click.command()
@click.option('-s', '--save', type=str, help='save to file')
@click.argument('json_path_or_data', type=str)
@click.argument('input_format', type=click.Choice(services.keys()))
@click.argument('output_format', type=click.Choice(output_choices))
def cli(save, 
        json_path_or_data,
        input_format,
        output_format):

    if not helpers.is_path(json_path_or_data):
        json_data = json.loads(json_path_or_data)
    else:
        with open(json_path_or_data) as fin:
            json_data = json.load(fin)
    service = services[input_format]
    converter = service(json_data)
    converter.convert()
    if save:
        path = save
        converter.save(path, output_format)
        click.echo(f'{path} saved.')
    else:
        output_formatter = getattr(converter, output_format)
        click.echo(output_formatter())
