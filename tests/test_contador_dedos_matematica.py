import os
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from contador_dedos_matematica import ContadorDedosMatematica


class DummyLandmark:
    def __init__(self, x=0.5, y=0.5):
        self.x = x
        self.y = y


class DummyClassification:
    def __init__(self, label: str):
        self.label = label


class DummyHandedness:
    def __init__(self, label: str):
        self.classification = [DummyClassification(label)]


def create_landmarks(thumb_tip_x: float, thumb_ip_x: float, fingers_up):
    landmarks = [DummyLandmark() for _ in range(21)]
    landmarks[4].x = thumb_tip_x
    landmarks[3].x = thumb_ip_x

    tip_ids = [8, 12, 16, 20]
    pip_ids = [6, 10, 14, 18]

    for is_up, tip_id, pip_id in zip(fingers_up, tip_ids, pip_ids):
        if is_up:
            landmarks[tip_id].y = 0.4
            landmarks[pip_id].y = 0.6
        else:
            landmarks[tip_id].y = 0.7
            landmarks[pip_id].y = 0.5

    return landmarks


class TestContadorDedosMatematica(unittest.TestCase):
    def test_gerar_nova_pergunta_reseta_estado(self):
        app = ContadorDedosMatematica()
        app.acertou = True
        app.mostrar_botao = True
        app.tempo_inicio_pergunta = 0

        with patch(
            "contador_dedos_matematica.random.randint", side_effect=[7, 3]
        ):
            app.gerar_nova_pergunta()

        self.assertEqual(app.resposta_correta, 7)
        self.assertEqual(app.num1, 3)
        self.assertEqual(app.num2, 4)
        self.assertFalse(app.acertou)
        self.assertFalse(app.mostrar_botao)
        self.assertGreater(app.tempo_inicio_pergunta, 0)

    def test_contar_dedos_mao_direita_todos_levantados(self):
        app = ContadorDedosMatematica()
        landmarks = create_landmarks(0.1, 0.2, [True, True, True, True])
        handedness = DummyHandedness("Right")

        total_dedos = app.contar_dedos(landmarks, handedness)

        self.assertEqual(total_dedos, 5)

    def test_contar_dedos_mao_esquerda_polegar_para_baixo(self):
        app = ContadorDedosMatematica()
        landmarks = create_landmarks(0.1, 0.2, [True, True, True, True])
        handedness = DummyHandedness("Left")

        total_dedos = app.contar_dedos(landmarks, handedness)

        self.assertEqual(total_dedos, 4)

    def test_contar_dedos_mao_esquerda_com_polegar_levantado(self):
        app = ContadorDedosMatematica()
        landmarks = create_landmarks(0.3, 0.2, [False, False, False, False])
        handedness = DummyHandedness("Left")

        total_dedos = app.contar_dedos(landmarks, handedness)

        self.assertEqual(total_dedos, 1)


if __name__ == "__main__":
    unittest.main()
