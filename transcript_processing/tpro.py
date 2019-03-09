import json

import click

from .converters import services
from . import outputs
from . import helpers

output_choices =  [k for k, v in 
                   outputs.__dict__.items()
                   if callable(v)]

@click.command()
@click.option('-p', '--print-output', is_flag=True, default=True,
        help='pretty print the transcript, breaks pipeability')
@click.argument('transcript_data_path', type=click.File('r'))
@click.argument('output_path', type=click.Path(writable=True, dir_okay=False))
@click.argument('input_format', type=click.Choice(services.keys()))
@click.argument('output_format', type=click.Choice(output_choices))
def cli(print_output,
        transcript_data_path,
        output_path,
        input_format,
        output_format):

    transcript_data_file_handle = transcript_data_path

    service = services[input_format]
    if service.transcript_type == dict:
        transcript_data = json.load(transcript_data_file_handle)
    else:
        transcript_data = transcript_data_file_handle.read()

    converter = service(transcript_data)
    converter.convert()
    converter.save(output_path, output_format)

    if print_output:
        with open(output_path) as fin:
            click.echo(fin.read())

    click.echo(f'☝☝☝ There\'s your transcript, which was saved to {output_path}.')
