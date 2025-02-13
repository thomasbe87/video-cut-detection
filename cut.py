import cv2
import numpy as np
from datetime import datetime, timedelta
from mss import mss
import time
import csv
import os

# ----------------------------
# CONSTANTES GLOBALES
# ----------------------------
THRESHOLD_DEFAULT = 30.0 #seuil de détection
MIN_TIME_BETWEEN_CUTS_DEFAULT = 0.8 #seconde minimum entre deux captures

class SceneDetector:
    def __init__(self, threshold=THRESHOLD_DEFAULT, min_time_between_cuts=MIN_TIME_BETWEEN_CUTS_DEFAULT):
        self.threshold = threshold
        self.min_time_between_cuts = min_time_between_cuts
        self.running = True
        self.cut_timestamps = []
        self.start_time = None
        self.last_cut_time = None
    
    def format_timestamp(self, seconds):
        total_seconds = int(seconds)
        milliseconds = int((seconds - total_seconds) * 10)
        return f"{str(timedelta(seconds=total_seconds))}.{milliseconds}"
        
    def analyze_screen(self):
        print("🔍 Démarrage de l'analyse...")
        print(f"📏 Seuil de détection: {self.threshold}")
        print(f"⏳ Délai minimum entre cuts: {self.min_time_between_cuts} secondes")
        print("🛑 Appuyez sur Ctrl+C pour arrêter")
        print("-----------------------------")
        
        try:
            with mss() as sct:
                monitor = sct.monitors[1]  # Capture l'écran principal (modifiez si besoin)
                
                self.start_time = datetime.now()
                self.last_cut_time = self.start_time
                prev_frame = None
                
                while self.running:
                    try:
                        # Capture d'écran
                        screenshot = np.array(sct.grab(monitor))
                        current_frame = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2GRAY)

                        # Appliquer un flou pour réduire les faux positifs
                        blurred_frame = cv2.GaussianBlur(current_frame, (1, 1), 0)

                        if prev_frame is not None:
                            # Calcul de la différence entre images successives
                            diff = cv2.absdiff(blurred_frame, prev_frame)
                            mean_diff = np.mean(diff)

                            current_time = datetime.now()
                            time_since_last_cut = (current_time - self.last_cut_time).total_seconds()

                            # Vérification si le seuil de changement est atteint et si le temps minimum est respecté
                            if mean_diff > self.threshold and time_since_last_cut >= self.min_time_between_cuts:
                                elapsed = (current_time - self.start_time).total_seconds()
                                timestamp = self.format_timestamp(elapsed)
                                print(f"Cut détecté à {timestamp}")
                                self.cut_timestamps.append(elapsed)
                                self.last_cut_time = current_time

                        prev_frame = blurred_frame
                        time.sleep(0.03)  # ~30 FPS, possibilité de réduire pour alléger la charge
                
                    except Exception as e:
                        print(f"⚠️ Erreur pendant l'analyse : {e}")
                    
        except KeyboardInterrupt:
            print("\n🛑 Arrêt demandé par l'utilisateur")
        except Exception as e:
            print(f"\n❌ Erreur critique : {str(e)}")
        finally:
            self.print_statistics()
            self.export_to_csv()
    
    def print_statistics(self):
        print("\n📊 Statistiques de l'analyse:")
        total_time = (datetime.now() - self.start_time).total_seconds() if self.start_time else 0
        print(f"⏲️ Durée totale : {self.format_timestamp(total_time)}")
        print(f"🎬 Nombre de cuts détectés : {len(self.cut_timestamps)}")
        
        if self.cut_timestamps:
            intervals = np.diff(self.cut_timestamps)
            print(f"⏳ Temps moyen entre les cuts : {self.format_timestamp(np.mean(intervals))}")
            print(f"📈 Fréquence : {len(self.cut_timestamps) / total_time * 60:.2f} cuts/minute")
    
    def export_to_csv(self):
        # Créer un nom de fichier avec la date et l'heure
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"scene_analysis_{timestamp}.csv"
        
        # Calculer les intervalles entre les cuts
        intervals = np.diff(self.cut_timestamps) if len(self.cut_timestamps) > 1 else []
        total_time = (datetime.now() - self.start_time).total_seconds() if self.start_time else 0
        
        try:
            with open(filename, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Type', 'Valeur'])
                writer.writerow(['Seuil de détection', f"{self.threshold}"])
                writer.writerow(['Durée totale (secondes)', f"{total_time:.1f}"])
                writer.writerow(['Nombre de cuts', len(self.cut_timestamps)])
                writer.writerow(['Fréquence (cuts/minute)', f"{len(self.cut_timestamps) / total_time * 60:.2f}"])
                
                if len(intervals) > 0:
                    writer.writerow(['Temps moyen entre cuts (secondes)', f"{np.mean(intervals):.1f}"])
                    writer.writerow(['Temps minimum entre cuts (secondes)', f"{np.min(intervals):.1f}"])
                    writer.writerow(['Temps maximum entre cuts (secondes)', f"{np.max(intervals):.1f}"])
                
                writer.writerow([])
                writer.writerow(['Liste des cuts'])
                writer.writerow(['Numéro', 'Timestamp'])
                for i, ts in enumerate(self.cut_timestamps, 1):
                    writer.writerow([i, f"{ts:.1f}"])
            
            print(f"\n✅ Statistiques exportées dans : {filename}")
        
        except Exception as e:
            print(f"❌ Erreur lors de l'export CSV : {e}")

# ----------------------------
# PROGRAMME PRINCIPAL
# ----------------------------
if __name__ == "__main__":
    detector = SceneDetector(THRESHOLD_DEFAULT, MIN_TIME_BETWEEN_CUTS_DEFAULT)
    detector.analyze_screen()