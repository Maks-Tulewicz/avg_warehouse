.PHONY: build up down shell logs clean test gazebo rosdep

# Budowanie obrazu
build:
	docker compose build

# Uruchomienie kontenera
up:
	docker compose up -d

# Wejście do kontenera
shell:
	docker exec -it ros2_humble_dev bash

# Wejście do kontenera z automatycznym sourcingiem ROS
ssh:
	docker exec -it ros2_humble_dev bash -c "source /opt/ros/humble/setup.bash && bash"

# Zatrzymanie kontenera
down:
	docker compose down

# Wyświetlanie logów
logs:
	docker compose logs -f ros_dev

# Czyszczenie cache'u
clean:
	rm -rf build install log
	docker compose down -v

# Uruchomienie testów w kontenerze
test:
	docker exec ros2_humble_dev python3 -m pytest tests/ -v --tb=short

# Testy z coverage
test-cov:
	docker exec ros2_humble_dev python3 -m pytest tests/ -v --cov=src --cov-report=html

# Budowanie ROS 2 packages
colcon-build:
	docker exec ros2_humble_dev bash -c "source /opt/ros/humble/setup.bash && cd /ros2_ws/src/ros2 && colcon build --symlink-install"

# Testowanie ROS 2 packages
colcon-test:
	docker exec ros2_humble_dev bash -c "source /opt/ros/humble/setup.bash && cd /ros2_ws/src/ros2 && colcon test"

# Uruchomienie symulacji Gazebo (wymaga GUI)
gazebo:
	docker exec -it ros2_humble_dev bash -c "source /opt/ros/humble/setup.bash && ros2 launch robot_controller simulation.launch.py"

# Uruchomienie symulacji DISCRETE-EVENT (bez Gazebo, czysty Python)
simulate:
	docker exec ros2_humble_dev python3 scripts/run_simulation.py --robots 10 --orders 50 --duration 3600

# Uruchomienie wizualizacji stanu
visualize:
	docker exec -it ros2_humble_dev python3 scripts/visualize_state.py

# Instalacja zależności ROS 2 (rosdep)
rosdep:
	docker exec ros2_humble_dev bash -c "source /opt/ros/humble/setup.bash && cd /ros2_ws && rosdep install --from-paths src/ros2 --ignore-src -r -y"

# Full pipeline: build + test + lint
ci: lint test
	@echo "CI checks passed!"

# Linting
lint:
	docker exec ros2_humble_dev bash -c "flake8 src/ && black --check src/ tests/"

# Formatting (naprawia błędy)
fmt:
	docker exec ros2_humble_dev bash -c "black src/ tests/ && isort src/ tests/"