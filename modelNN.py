import snake
import tensorflow as tf
import numpy as np
import random
import math


class SnakeNN:

    def create_model(self):
        model = tf.keras.Sequential([tf.keras.layers.Dense(520, activation='relu'),
                                     tf.keras.layers.Dense(520, activation='relu'),
                                     tf.keras.layers.Dense(520, activation='relu'),
                                     tf.keras.layers.Dense(520, activation='linear'),
                                     tf.keras.layers.Dense(3)
                                     ])

        model.compile(optimizer='adam',
                      loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                      metrics=['sparse_categorical_accuracy'])

        return model

    def get_best_option_for_move(self, probability_model, status):
        predictions = []
        for i in range(-1, 2):
            predictions.append(
                probability_model.predict(np.array([status[0], status[1], status[2], status[3], status[4],
                                                    status[5], status[6], status[7], status[8], status[9], status[10],
                                                    i]).reshape(-1, 12)))
        possibilities = np.array(predictions).reshape(-1, 9)
        best_effect = [possibilities[0][2], possibilities[0][5], possibilities[0][8]]
        return random.choices([-1, 0, 1], best_effect, k=1)


    def rate_move(self, is_snake_dead, distance_before, distance_after):
        if is_snake_dead:
            return 0
        else:
            if distance_before > distance_after:
                return 2
            else:
                return 1

    def train(self, repeats, predict_model, is_shown, model, probability_model, snake_size):
        movement_history = []
        movement_effect = []
        for i in range(repeats):
            print(f"Game: {i + 1}")
            game = snake.Snake(12, snake_size)
            while not game.is_snake_dead():
                status = game.check_status()
                distance_before = game.get_distance_to_apple()
                if predict_model == "random":
                    move = random.choice([-1, 0, 1])
                    number_of_epochs = 3
                else:
                    move = self.get_best_option_for_move(probability_model, status)[0]
                    number_of_epochs = 10
                game.game_step(is_shown, move)
                distance_after = game.get_distance_to_apple()
                movement_history.insert(0, np.concatenate((status, [move])))
                movement_effect.insert(0, self.rate_move(game.is_snake_dead(), distance_before, distance_after))
            print(game.score)
        model.fit(np.array(movement_history).reshape(-1, 12), np.array(movement_effect).reshape(-1, 1),
                  epochs=number_of_epochs,
                  shuffle=True)
        movement_history.clear()
        movement_effect.clear()

    def main(self):

        model = self.create_model()
        probability_model = tf.keras.Sequential([model, tf.keras.layers.Softmax()])

        self.train(50, "random", False, model, probability_model, 6)
        for i in range(1):
            self.train(4, "NN", True, model, probability_model, 3)



SnakeNN().main()
