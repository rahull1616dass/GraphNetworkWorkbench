from requests import get as http_get
from pandas import DataFrame, read_csv
from requests import Response as RequestsResponse

from core.typing import MLTask

def get_data_frame(file_url: str) -> DataFrame:
    file_response: RequestsResponse = http_get(
        file_url, stream=True, headers={"Content-Type": "text/csv"}
    )
    print(file_response.status_code)
    if file_response.status_code != 200:
        raise Exception(
            f"""
              Error downloading file at {file_url}
              Reason: {file_response.reason}
              Text: {file_response.text}
            """
        )
    # Parse the csv in file_response.raw with np.genfromtxt
    return read_csv(file_response.raw)


def download_network_files(task: MLTask) -> dict[str, DataFrame]:
    return {
        'nodes': get_data_frame(task.nodes_file_url),
        'edges': get_data_frame(task.edges_file_url),
    }
