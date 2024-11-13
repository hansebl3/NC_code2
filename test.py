import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# NC 코드에서 X, Y, Z 좌표 추출하는 함수
def parse_nc_code(file_path):
    positions = []  # 좌표 리스트
    x = y = z = 0   # 초기 좌표 (0, 0, 0)

    with open(file_path, 'r') as file:
        for line in file:
            parts = line.split()
            for part in parts:
                if part.startswith('X'):
                    x = float(part[1:])
                elif part.startswith('Y'):
                    y = float(part[1:])
                elif part.startswith('Z'):
                    z = float(part[1:])
            
            # G1 또는 G0 명령에 해당하는 좌표를 기록 (이동 명령만 추출)
            if 'G1' in parts or 'G0' in parts:
                positions.append([x, y, z])

    return np.array(positions)

# 벡터 길이를 계산하는 함수
def calculate_vector_length(v1, v2):
    return np.linalg.norm(v2 - v1)

# 벡터의 속도 계산 함수
def calculate_velocity(v1, v2, delta_time=1):
    length = calculate_vector_length(v1, v2)
    return length / delta_time  # 속도 = 거리 / 시간 (시간 간격은 1로 가정)

# NC 코드 파일에서 좌표 추출
nc_code_file = 'c:/py/works/1.nc'
positions = parse_nc_code(nc_code_file)

# 3D 플롯 생성
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# 속도를 계산하고 벡터 그리기
velocities = []
for i in range(1, len(positions)):
    v1 = positions[i - 1]
    v2 = positions[i]
    velocity = calculate_velocity(v1, v2)  # 속도 계산
    velocities.append(velocity)
    ax.plot([v1[0], v2[0]], [v1[1], v2[1]], [v1[2], v2[2]], marker='o', color=plt.cm.viridis(velocity / max(velocities)))  # 속도에 따라 색상 변화

# 속도 레이블 추가 (속도 범위)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('3D NC Code Path with Speed Visualization')

# 플롯 표시
plt.show()