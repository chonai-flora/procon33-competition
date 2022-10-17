import numpy as np
import glob
import librosa
import pydub
from pydub import AudioSegment
from typing import Union, List

# 音源読み込み
def load_audio(file_name: str, sr: int) -> np.ndarray:
    return librosa.load(file_name, sr=sr, mono=True)[0]


# 読みデータ一括読み込み
def load_audios(lang: str, sr: int) -> List[np.ndarray]:
    if lang != 'J' and lang != 'E':
        print("ファイルが見つかりません")
        return []
    
    audio_dir = './JKspeech/'
    file_names = glob.glob(f'{audio_dir}/{lang}*.wav')
    return [load_audio(file_name, sr) for file_name in file_names]


# AudioSegmentに変換
def to_AudioSegment(file_name: str) -> Union[AudioSegment, None]:
    try:
        audio_segment = AudioSegment.from_file(file_name, format="wav")
        return audio_segment
    except FileNotFoundError as e:
        print(e)
    return None


# 畳み込みで適合率を求める
def get_precision(origin_init: np.ndarray, target_init: np.ndarray) -> np.ndarray:
    # サイズ調整
    start = np.abs(len(origin_init) - len(target_init)) / 180
    start = np.min([int(start), 640])
    end = np.min([len(origin_init), len(target_init)])
    target = target_init[start:end]
    origin = origin_init[start:end]

    # フーリエ変換
    fft_O = np.fft.fft(origin)
    fft_T = np.fft.fft(target)

    # 畳み込み処理
    fft_Oc = np.conj(fft_O)  # 複素共役を取る
    sigma_C = fft_Oc * fft_T  # 要素ごとに乗算
    sigma_T = np.fft.ifft(sigma_C)  # 逆フーリエ変換
    sigma_T = np.abs(sigma_T)  # 絶対値を取りスカラー値に変換
    
    return np.max(sigma_T)  # スカラー値の最大値


# 仮名->ナンバー, ナンバー->仮名
def kana_to_number(kana: str) -> int:
    s = "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをん"
    return s.index(kana) + 1

def number_to_kana(number: int) -> str:
    s = "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをん"
    return s[number - 1]
