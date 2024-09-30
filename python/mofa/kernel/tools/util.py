import os

import yfinance as yf
import torch
# import whisper
from crewai_tools.tools.txt_search_tool.txt_search_tool import TXTSearchTool


def stock_data(symbol:str,start_date:str,end_date:str):
    """
    Collect price, volume, and market trend data for a specified stock within a specified date range.

    Parameters:
    symbol (str): Stock symbol, e.g., 'NVDA' for NVIDIA, 'TSLA' for Tesla.
    start_date (str): Start date for data collection, in the format 'YYYY-MM-DD'.
    end_date (str): End date for data collection, in the format 'YYYY-MM-DD'.

    Returns:
    Pandas DataFrame: Contains price, volume, and market trend data for the specified stock within the specified date range.

    Example:
    data = stock_data('NVDA', '2023-01-01', '2023-12-31')
    """

    data = yf.download(symbol, start=start_date, end=end_date)
    if data.empty:
        raise ValueError(f"No data found for symbol: {symbol} from {start_date} to {end_date}")
    return data

# def whisper_translate_audio(audio_file:str,module_file:str=None,language:str=None,save_file:str='./output/audio_file.txt')->str:
#     """
#     This function uses the Whisper model to transcribe an audio file into Chinese text and saves the result to a specified file.
#
#     Parameters
#     audio_file (str): Path to the audio file to be transcribed.
#     module_file (str): Whisper model version to use, default is 'medium'.
#     language (str): Language for transcription, default is 'Chinese'.
#     save_file (str): Path to save the transcribed text file, default is './output/audio_file.txt'.
#     Return Value
#     Returns the transcribed text content (str).
#     """
#     device = "cuda" if torch.cuda.is_available() else "cpu"
#     if module_file == None:
#         module_file = 'base'
#     model = whisper.load_model(module_file).to(device)
#     if language is None or language == 'English':
#         result = model.transcribe(audio_file)
#     else:
#         result = model.transcribe(audio_file,
#                                   language=language)
#     if save_file is not None:
#         dir_path = os.path.dirname(save_file)
#         if not os.path.exists(dir_path):
#             os.makedirs(dir_path)
#         with open(save_file, "w") as f:
#             f.write(result['text'])
#     return result['text']

def text_rag(file_path:str):
    """

    Uses the TXTSearchTool to perform a Retrieval-Augmented Generation (RAG) task on the text file specified by the file_path.

    Parameters:
    file_path (str): The path to the text file that will be processed using the TXTSearchTool.

    """

    return TXTSearchTool(txt=file_path)