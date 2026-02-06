import numpy as np
import matplotlib.pyplot as plt

def preprocess_4_plot():
    age = [23,23,27,27,39,41,47,49,50,52,54,54,56,57,58,58,60,61]
    fat = [9.5,26.5,7.8,17.8,31.4,25.9,27.2,27.2,31.2,34.6,42.5,28.8,33.4,30.2,34.1,32.9,41.2,35.7]

    fig, axs = plt.subplots(2, 2, figsize=(12, 8))
    axs[0, 0].hist(age)
    axs[0, 0].set_xlabel("Age")
    axs[0, 0].set_ylabel("Frequency")
    axs[0, 0].set_title("Age Distribution")
    axs[0, 1].boxplot(age)
    axs[0, 1].set_ylabel("Age")
    axs[0, 1].set_title("Age Boxplot")
    axs[1, 0].scatter(age, fat)
    axs[1, 0].set_xlabel("Age")
    axs[1, 0].set_ylabel("Fat")
    axs[1, 0].set_title("Scatter plot Age vs Fat")
    axs[1, 1].scatter(np.sort(age), np.sort(fat))
    axs[1, 1].set_xlabel("Age")
    axs[1, 1].set_ylabel("Fat")
    axs[1, 1].plot([min(age), max(age)], [min(fat), max(fat)], color='red', linestyle='--')
    axs[1, 1].set_title("QQ plot Age vs Fat")
    plt.savefig("img/preprocess_plot.pdf")
    plt.show()


if __name__ == "__main__":
    preprocess_4_plot()