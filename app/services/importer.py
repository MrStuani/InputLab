import csv
import io
import json

MAX_FILE_BYTES = 5 * 1024 * 1024   # 5 MB
LATENCY_COLUMN = "latency"          # TODO: troque pelo nome real da coluna no seu CSV


class ImportFailure(ValueError):
    """Erro de importação com mensagem amigável."""


def parse_samples(filename: str, content: bytes) -> list[float]:
    if len(content) > MAX_FILE_BYTES:
        raise ImportFailure("Arquivo maior que 5 MB")
    text = content.decode("utf-8-sig")
    name = filename.lower()
    if name.endswith(".csv"):
        return _parse_csv(text)
    if name.endswith(".json"):
        return _parse_json(text)
    raise ImportFailure("Formato não suportado (use .csv ou .json)")


def _parse_csv(text: str) -> list[float]:
    reader = csv.DictReader(io.StringIO(text))
    if reader.fieldnames is None or LATENCY_COLUMN not in reader.fieldnames:
        raise ImportFailure(f"Coluna '{LATENCY_COLUMN}' não encontrada")
    values = []
    for line_no, row in enumerate(reader, start=2):
        try:
            values.append(float(row[LATENCY_COLUMN]))
        except (TypeError, ValueError):
            raise ImportFailure(f"Valor inválido na linha {line_no}")
    return values


def _parse_json(text: str) -> list[float]:
    # TODO: ajuste para a estrutura real do seu export
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        raise ImportFailure("JSON inválido")
    if isinstance(data, dict):
        data = data.get("samples")
    if not isinstance(data, list) or not data:
        raise ImportFailure("JSON sem lista de amostras")
    try:
        return [float(v) for v in data]
    except (TypeError, ValueError):
        raise ImportFailure("JSON contém valores não numéricos")