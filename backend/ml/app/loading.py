from requests import get as http_get
from pandas import DataFrame, read_csv
from requests import Response as RequestsResponse

from app.typing import MLRequest


def get_data_frame(file_url: str, create_index: bool = True) -> DataFrame:
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


def download_network_files(request: MLRequest) -> dict[str, DataFrame]:
    if request.nodes_file_url is None:
        raise Exception("No nodes file url found")
    elif request.edges_file_url is None:
        raise Exception("No edges file url found")

    return {
        'nodes': get_data_frame(request.nodes_file_url, create_index=False),
        'edges': get_data_frame(request.edges_file_url, create_index=False),
    }
