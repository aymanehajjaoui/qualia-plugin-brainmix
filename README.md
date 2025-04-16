# Qualia Plugin: BrainMIX

This plugin adds custom deployment targets for the RedPitaya board to the [Qualia](https://github.com/LEAT-EDGE/qualia-core) framework.

## Features

- `RedPitaya`: Deploys the model to run on RedPitaya (compiled on PC).
- `RedPitaya_App`: Exports a full application template with the model for native build directly on the board.
- `RedPitaya_Metrics`: Extends `RedPitaya` by adding GPIO control to trigger energy consumption measurement using the Otii Arc (currently under testing; requires a working cross-compiler for RedPitaya).

## Installation

```bash
git clone https://github.com/aymanehajjaoui/qualia-plugin-brainmix.git
cd qualia-plugin-brainmix
uv pip install -e .
```
