# **llm-liaa-payment-receipt**

<p align="center"> 🚀 This script is designed to masking sensitive data from payment receipts of Pix</p>
<p align="center">It includes auxiliary scripts to organize, count, and create the coordinates of sensitive data locations in the templates</p>

The workflow for receiving a new payment receipt is described in the image below.

![new_payment_receipt_flow.png](./docs/new_payment_receipt_flow.png)

<h3>🏁 Table of Contents</h3>

<br>

===================

<!--ts-->

💻 [Dependencies and Environment](#dependenciesandenvironment)

☕ [Using](#using)

👷 [Author](#author)

<!--te-->

===================

<div id="dependenciesandenvironment"></div>

## 💻 **Dependencies and Environment**

### Prerequisites

- Python 3.8+
- Virtual environment tool ([venv](https://docs.python.org/pt-br/3.13/library/venv.html) recommended)
- Gemini API Key (for image template matching and guardrails execution)

### Setup

#### 1. Create and Activate Virtual Environment

```bash
$ make setup
```

This creates a `.venv` directory with all dependencies installed.

Activate it:

```bash
$ source .venv/bin/activate
```

#### 2. Configure Gemini API (Required for Template Matching)

**⚠️ Important:** Use the **PAID Google Gemini API** to ensure sensitive payment data is not logged or retained.

1. Get your API key: https://aistudio.google.com/apikey
2. Create a `.env` file in the project root:

```
GEMINI_API_KEY=your_api_key_here
```

The script will automatically load this variable.

#### 3. Clean Up

```bash
$ make clean
```

<div id="using"></div>

## ☕ **Using**

First, check the [dependencies](#dependenciesandenvironment) process

To check utility scripts, verify [scripts/README.md](/scripts/README.md)

### 📊 How the Project Works

Key Components

| Component                       | Purpose                                   |
| ------------------------------- | ----------------------------------------- |
| `config/coordinates/`           | Stores coordinate templates for each bank |
| `scripts/create_coordinates.py` | Interactive tool to create new templates  |
| `main.py`                       | Main execution script for anonimization   |
| `src/usecases/masking.py`       | Applies black masks to coordinates        |
| `src/usecases/matcher.py`       | Matches receipt to best template          |
| `src/usecases/guardrails.py`    | Validates masking quality                 |

This project operates in a **two-stage workflow**:

#### **Stage 1: Template Creation** 🗂️

Before you can mask, you need to create **coordinate templates**. These templates map the exact locations of sensitive data on the inputs (images or PDFs).

**To create templates:**

```bash
$ python scripts/create_coordinates.py -i 'path/to/receipt.png' -o 'src/config/coordinates/bankname/coordinates_output_1.json'
```

This opens an interactive window where you:

- **Draw rectangles** around sensitive data areas with your mouse
- **Press `u`** to undo the last rectangle
- **Press `r`** to reset all rectangles
- **Press `q`** to finish and save

The coordinates are saved in JSON format with `{x, y, width, height}` for each sensitive area.

#### **Stage 2: Anonimization** 🚀

Once you have templates, you can anonimize receipts by running the main script. It will:

1. Load the coordinate templates for the detected bank
2. Match the receipt to the most similar template
3. Apply black masks to all sensitive data areas
4. Run guardrails to verify no sensitive data remains

**For a single file** (specify the bank name):

```bash
$ python main.py -i 'example.jpeg' -n '99pay'
```

**For a directory** (automatically detects bank from folder structure):

```bash
$ python main.py -i 'dataset'
```

Ensure the folder structure follows this pattern:

```
dataset/
├── Glener/
│   └── nu/
│       └── receipt_1.png
└── João/
    ├── xp/
    │   └── receipt_1.png
    │   └── receipt_2.pdf
    └── bb/
        └── receipt_1.jpg
```

**Output structure** (same as input):

```
output/
├── Glener/
│   └── nu/
│       └── receipt_1.png (✓ masked)
└── João/
    ├── xp/
    │   └── receipt_1.png (✓ masked)
    │   └── receipt_2.pdf (✓ masked)
    └── bb/
        └── receipt_1.jpg (✓ masked)
```

### 📁 Available Bank Templates

Templates are stored in `src/config/coordinates/` organized by bank:

- `99pay/`
- `banrisul/`
- `bb/`
- `caixa/`
- `inter/`
- `itau/`
- `mercadopago/`
- `next/`
- `nu/`
- `picpay/`
- `santander/`
- `sicredi/`
- `xp/`

**Note:** If processing a file from a bank without templates, it will be skipped automatically.

**Important!** Note that the coordinate structure is specific to the anonymization of Pix payment receipts by payment institution. Feel free to edit the organization and consumption of the coordinates for your specific problem.

<div id="author"></div>

#### **👷 Author**

Made by Glener Pizzolato! 🙋

[![Linkedin Badge](https://img.shields.io/badge/-Glener-blue?style=flat-square&logo=Linkedin&logoColor=white&link=https://www.linkedin.com/in/glener-pizzolato/)](https://www.linkedin.com/in/glener-pizzolato-6319821b0/)
[![Gmail Badge](https://img.shields.io/badge/-glenerpizzolato@gmail.com-c14438?style=flat-square&logo=Gmail&logoColor=white&link=mailto:glenerpizzolato@gmail.com)](mailto:glenerpizzolato@gmail.com)
