import numpy as np
import pygame
import os
from classes import Robot, Graphics
import utils

def setup_mode():
    """Robot ve sensörlerin konumlandırılması için kurulum modu"""
    # Robot parametreleri
    ROBOT_WIDTH = 0.17  # Robot gövdesinin genişliği (metre)
    INITIAL_MOTOR_SPEED = 150  # Başlangıç motor hızı (rpm)
    MAX_MOTOR_SPEED = 312.5  # Maksimum motor hızı (rpm)
    WHEEL_RADIUS = 0.016  # Tekerlek yarıçapı (metre)
    SENSORS_NUMBER = 8  # Sensör sayısı
    SENSOR_COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255),
                    (255, 255, 0), (0, 255, 255), (255, 0, 255),
                    (255, 255, 255), (128, 0, 0), (0, 128, 0),
                    (0, 0, 128), (0, 128, 128)]

    # Mevcut kurulum dosyası kontrolü
    if os.path.isfile('setup.txt'):
        print('\n\nMevcut bir setup.txt dosyası bulundu.')
        print('Üzerine yazmak istiyor musunuz? (e/h)')
        answer = input()
        while answer.lower() not in ['e', 'h']:
            print('Geçersiz giriş. Lütfen \'e\' veya \'h\' yazın.')
            answer = input()
        
        if answer.lower() != 'e':
            return

    # Harita başlatma
    pygame.init()
    infoObject = pygame.display.Info()
    MAP_DIMENSIONS = (infoObject.current_w - 30, infoObject.current_h - 100)
    gfx = Graphics(MAP_DIMENSIONS, 'images/robot.png', 'images/map.png')

    # Robot konumlandırma
    ROBOT_START, closed = gfx.robot_positioning()

    # Sensör konumlandırma
    SENSORS_POSITIONS, closed = gfx.sensors_positioning(SENSORS_NUMBER, ROBOT_START, closed)

    if not closed:
        gfx.show_important_message("Kurulum tamamlandı! Kaydediliyor ve çıkılıyor...")
        pygame.display.update()
        pygame.time.wait(1500)
        
        # Kurulum bilgilerini kaydet
        setup_info = f"""{ROBOT_WIDTH}
        {INITIAL_MOTOR_SPEED}
        {MAX_MOTOR_SPEED}
        {WHEEL_RADIUS} 
        {SENSORS_NUMBER}
        {MAP_DIMENSIONS}
        {ROBOT_START}
        {SENSORS_POSITIONS}
        {SENSOR_COLORS}
        """
        utils.write_setup_file(setup_info)
    else:
        print("\033[91m {}\033[00m" .format("\nKurulum tamamlanmadı! Kaydetmeden çıkılıyor...\n"))

def run_mode():
    """Robot simülasyonunu çalıştırma modu"""
    # Kurulum dosyasını oku
    setup_info = utils.read_setup_file()
    
    # Parametreleri ayarla
    ROBOT_WIDTH = setup_info[0]
    INITIAL_MOTOR_SPEED = setup_info[1]
    MAX_MOTOR_SPEED = setup_info[2]
    WHEEL_RADIUS = setup_info[3]
    SENSORS_NUMBER = setup_info[4]
    MAP_DIMENSIONS = setup_info[5]
    ROBOT_START = setup_info[6]
    SENSORS_POSITIONS = setup_info[7]
    SENSOR_COLORS = setup_info[8]

    # Harita ve robot başlatma
    gfx = Graphics(MAP_DIMENSIONS, 'images/robot.png', 'images/map.png')
    robot = Robot(initial_position=ROBOT_START,
                  width=ROBOT_WIDTH,
                  initial_motor_speed=INITIAL_MOTOR_SPEED,
                  max_motor_speed=MAX_MOTOR_SPEED,
                  wheel_radius=WHEEL_RADIUS)

    # Sensörleri başlat
    for position in SENSORS_POSITIONS:
        robot.add_sensor(position, ROBOT_START)

    # Simülasyon değişkenleri
    last_time = pygame.time.get_ticks()
    last_error = 0
    I = 0  # PID integral
    running = True

    pygame.font.init()
    font = pygame.font.SysFont("Arial", 18)

    while running:
        # Pencere kapatma kontrolü
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Harita ve robot çizimi
        gfx.map.blit(gfx.map_image, (0, 0))
        gfx.draw_robot(robot.x, robot.y, robot.heading)
        
        # Sensörleri çiz
        for sensor in robot.sensors:
            gfx.draw_sensor(sensor, color=SENSOR_COLORS[robot.sensors.index(sensor)])
        
        # Sensör verilerini oku
        for idx in range(len(robot.sensors)):
            robot.sensors[idx].read_data(gfx.map_image)
        
        # Sensör verilerini göster
        gfx.show_sensors_data(robot.sensors, sensor_colors=SENSOR_COLORS[:SENSORS_NUMBER])

        # Zaman hesaplama
        current_time = pygame.time.get_ticks()
        dt = (current_time - last_time)/1000
        last_time = current_time

        # Kontrol mantığı
        left_error = sum([robot.sensors[i].data for i in range(4)])
        right_error = sum([robot.sensors[i].data for i in range(4, 8)])
        error = left_error - right_error

        # PID hesaplama
        pid, I = utils.PID(kp=50, ki=3, kd=0.01, I=I, error=error, last_error=last_error, dt=dt)
        last_error = error

        # Motor hızlarını güncelle
        left_motor_speed = robot.left_motor.max_motor_speed + pid
        right_motor_speed = robot.right_motor.max_motor_speed - pid
        robot.left_motor.set_speed(left_motor_speed)
        robot.right_motor.set_speed(right_motor_speed)
        
        # Robot ve sensör pozisyonlarını güncelle
        robot.update_position(dt)
        for idx in range(len(robot.sensors)):
            robot.sensors[idx].update_position(
                robot_position=(robot.x, robot.y, robot.heading),
                sensor_relative_position=SENSORS_POSITIONS[idx]
            )
        
        # Sınır kontrolü
        robot_is_out = gfx.is_out_of_bounds(robot)
        sensor_is_out = bool(np.sum([gfx.is_out_of_bounds(sensor) for sensor in robot.sensors]))
        
        if robot_is_out or sensor_is_out:
            gfx.show_important_message("Robot haritadan çıktı!")
            pygame.display.update()
            pygame.time.wait(3500)
            running = False
        
        if running:
            # Bilgileri ekranda göster
            error_text = font.render(f"Hata: {error:.2f}", True, (255, 0, 0))
            gfx.map.blit(error_text, (10, 250))
            
            pid_text = font.render(f"PID: {pid:.2f}", True, (0, 255, 0))
            gfx.map.blit(pid_text, (10, 280))
            
            left_motor_text = font.render(f"Sol Motor: {left_motor_speed:.2f}", True, (0, 0, 255))
            gfx.map.blit(left_motor_text, (10, 310))
            
            right_motor_text = font.render(f"Sağ Motor: {right_motor_speed:.2f}", True, (0, 0, 255))
            gfx.map.blit(right_motor_text, (10, 340))
            
            pygame.display.update()

def main():
    while True:
        print("\nÇizgi Takipçi Simülasyonu")
        print("1. Kurulum")
        print("2. Çalıştır")
        print("3. Çıkış")
        
        choice = input("\nSeçiminiz (1-3): ")
        
        if choice == "1":
            setup_mode()
        elif choice == "2":
            if not os.path.isfile('setup.txt'):
                print("\nHata: Önce kurulum yapmalısınız!")
                continue
            run_mode()
        elif choice == "3":
            print("\nProgram sonlandırılıyor...")
            break
        else:
            print("\nGeçersiz seçim! Lütfen 1-3 arası bir sayı girin.")

if __name__ == "__main__":
    main() 