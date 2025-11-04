import cv2
import mediapipe as mp
import random
import time

class ContadorDedosMatematica:
    def __init__(self):
        # Inicializa MediaPipe Hands
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )
        self.mp_draw = mp.solutions.drawing_utils
        
        # Estado do jogo
        self.num1 = 0
        self.num2 = 0
        self.resposta_correta = 0
        self.gerar_nova_pergunta()
        
        # Estados
        self.acertou = False
        self.mostrar_botao = False
        self.tempo_inicio_pergunta = time.time()
        self.dedos_detectados = 0
        self.tempo_resposta_correta = 0
        
        # Cores
        self.COR_VERDE = (0, 255, 0)
        self.COR_AZUL = (255, 200, 0)
        self.COR_VERMELHO = (0, 0, 255)
        self.COR_BRANCO = (255, 255, 255)
        self.COR_PRETO = (0, 0, 0)
        
    def gerar_nova_pergunta(self):
        """Gera uma nova pergunta de soma com resultado máximo 10"""
        self.resposta_correta = random.randint(1, 10)
        self.num1 = random.randint(0, self.resposta_correta)
        self.num2 = self.resposta_correta - self.num1
        self.acertou = False
        self.mostrar_botao = False
        self.tempo_inicio_pergunta = time.time()
        
    def contar_dedos(self, landmarks, handedness):
        """Conta quantos dedos estão levantados em uma mão"""
        dedos = []
        
        # Verificar se é mão esquerda ou direita
        eh_mao_direita = handedness.classification[0].label == "Right"
        
        # Polegar (diferente dos outros dedos)
        # Para mão direita: polegar levantado se tip_x < ip_x
        # Para mão esquerda: polegar levantado se tip_x > ip_x
        tip_x = landmarks[4].x
        ip_x = landmarks[3].x
        
        if eh_mao_direita:
            dedos.append(1 if tip_x < ip_x else 0)
        else:
            dedos.append(1 if tip_x > ip_x else 0)
        
        # Outros dedos (indicador, médio, anelar, mindinho)
        # IDs: [8, 12, 16, 20] são as pontas
        # IDs: [6, 10, 14, 18] são as articulações PIP
        tip_ids = [8, 12, 16, 20]
        pip_ids = [6, 10, 14, 18]
        
        for tip_id, pip_id in zip(tip_ids, pip_ids):
            # Dedo levantado se a ponta está acima da articulação PIP
            if landmarks[tip_id].y < landmarks[pip_id].y:
                dedos.append(1)
            else:
                dedos.append(0)
        
        return sum(dedos)
    
    def desenhar_interface(self, frame):
        """Desenha a interface do jogo no frame"""
        h, w, _ = frame.shape
        
        # Fundo semi-transparente para a área de pergunta
        overlay = frame.copy()
        cv2.rectangle(overlay, (10, 10), (w - 10, 150), (50, 50, 50), -1)
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
        
        # Mostrar pergunta
        pergunta = f"{self.num1} + {self.num2} = ?"
        cv2.putText(frame, pergunta, (50, 80), 
                   cv2.FONT_HERSHEY_DUPLEX, 2.5, self.COR_AZUL, 4)
        
        # Mostrar contador de dedos detectados
        texto_dedos = f"Dedos: {self.dedos_detectados}"
        cv2.putText(frame, texto_dedos, (50, 130), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, self.COR_BRANCO, 2)
        
        # Se acertou, mostrar mensagem e botão
        if self.acertou:
            # Mensagem de parabéns
            overlay2 = frame.copy()
            cv2.rectangle(overlay2, (w//4, h//4), (3*w//4, h//2), self.COR_VERDE, -1)
            cv2.addWeighted(overlay2, 0.8, frame, 0.2, 0, frame)
            
            cv2.putText(frame, "PARABENS!", (w//4 + 40, h//4 + 60), 
                       cv2.FONT_HERSHEY_DUPLEX, 2, self.COR_BRANCO, 4)
            cv2.putText(frame, "Voce acertou!", (w//4 + 40, h//4 + 110), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1.2, self.COR_BRANCO, 2)
            
            # Botão "Próxima"
            if self.mostrar_botao:
                cv2.rectangle(frame, (w//3, 2*h//3), (2*w//3, 2*h//3 + 80), 
                            self.COR_AZUL, -1)
                cv2.rectangle(frame, (w//3, 2*h//3), (2*w//3, 2*h//3 + 80), 
                            self.COR_BRANCO, 3)
                cv2.putText(frame, "Proxima", (w//3 + 80, 2*h//3 + 55), 
                           cv2.FONT_HERSHEY_DUPLEX, 1.5, self.COR_BRANCO, 3)
                
                # Instrução
                cv2.putText(frame, "Pressione ESPACO ou clique no botao", 
                           (w//4 - 50, h - 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.8, self.COR_BRANCO, 2)
        else:
            # Instruções
            cv2.putText(frame, "Mostre a resposta com os dedos!", 
                       (50, h - 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, self.COR_BRANCO, 2)
        
        # Botão de sair
        cv2.putText(frame, "Pressione ESC para sair", (w - 350, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 200), 2)
        
        return frame
    
    def processar_clique(self, event, x, y, flags, param):
        """Processa cliques do mouse"""
        if event == cv2.EVENT_LBUTTONDOWN and self.mostrar_botao:
            h, w = param
            # Verifica se clicou no botão
            if w//3 <= x <= 2*w//3 and 2*h//3 <= y <= 2*h//3 + 80:
                self.gerar_nova_pergunta()
    
    def executar(self):
        """Executa o programa principal"""
        # Inicializa câmera
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        
        # Configurar callback do mouse
        cv2.namedWindow('Contador de Dedos - Matematica')
        
        print("=" * 60)
        print("CONTADOR DE DEDOS - APRENDENDO MATEMÁTICA")
        print("=" * 60)
        print("\nInstruções:")
        print("1. Mostre a resposta da soma usando seus dedos")
        print("2. O sistema detectará suas mãos em tempo real")
        print("3. Quando acertar, pressione ESPAÇO ou clique em 'Próxima'")
        print("4. Pressione ESC para sair")
        print("\nBom aprendizado! 🎓\n")
        
        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                print("Erro ao acessar a câmera")
                break
            
            # Espelhar frame para facilitar uso
            frame = cv2.flip(frame, 1)
            h, w, _ = frame.shape
            
            # Configurar callback com dimensões
            cv2.setMouseCallback('Contador de Dedos - Matematica', 
                                self.processar_clique, (h, w))
            
            # Converter para RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(rgb_frame)
            
            # Resetar contador de dedos
            self.dedos_detectados = 0
            
            # Processar detecção de mãos
            if results.multi_hand_landmarks and results.multi_handedness:
                for hand_landmarks, handedness in zip(results.multi_hand_landmarks, 
                                                      results.multi_handedness):
                    # Desenhar landmarks da mão
                    self.mp_draw.draw_landmarks(
                        frame, 
                        hand_landmarks, 
                        self.mp_hands.HAND_CONNECTIONS,
                        self.mp_draw.DrawingSpec(color=self.COR_VERDE, thickness=2, circle_radius=2),
                        self.mp_draw.DrawingSpec(color=self.COR_AZUL, thickness=2)
                    )
                    
                    # Contar dedos desta mão
                    dedos_mao = self.contar_dedos(hand_landmarks.landmark, handedness)
                    self.dedos_detectados += dedos_mao
            
            # Verificar resposta
            if not self.acertou and self.dedos_detectados == self.resposta_correta:
                # Pequeno delay para confirmar (evitar falsos positivos)
                if not hasattr(self, 'tempo_confirmacao'):
                    self.tempo_confirmacao = time.time()
                elif time.time() - self.tempo_confirmacao > 1.0:
                    self.acertou = True
                    self.tempo_resposta_correta = time.time()
                    delattr(self, 'tempo_confirmacao')
            else:
                if hasattr(self, 'tempo_confirmacao'):
                    delattr(self, 'tempo_confirmacao')
            
            # Mostrar botão após 1.5 segundos de acerto
            if self.acertou and time.time() - self.tempo_resposta_correta > 1.5:
                self.mostrar_botao = True
            
            # Desenhar interface
            frame = self.desenhar_interface(frame)
            
            # Mostrar frame
            cv2.imshow('Contador de Dedos - Matematica', frame)
            
            # Processar teclas
            key = cv2.waitKey(1) & 0xFF
            if key == 27:  # ESC
                break
            elif key == 32 and self.mostrar_botao:  # ESPAÇO
                self.gerar_nova_pergunta()
        
        # Limpar recursos
        cap.release()
        cv2.destroyAllWindows()
        self.hands.close()
        print("\nPrograma encerrado. Até logo! 👋")

if __name__ == "__main__":
    app = ContadorDedosMatematica()
    app.executar()
