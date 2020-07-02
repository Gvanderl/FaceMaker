import pickle
import PIL.Image
import numpy as np
import dnnlib
import dnnlib.tflib as tflib
from encoder.generator_model import Generator
import matplotlib.pyplot as plt
import config
from tqdm import tqdm

URL_FFHQ = 'https://drive.google.com/uc?id=1MEGjdvVpUsu1jB4zrXZN7Y4kBBOzizDQ'

tflib.init_tf()
with dnnlib.util.open_url(URL_FFHQ, cache_dir=config.cache_dir) as f:
    generator_network, discriminator_network, Gs_network = pickle.load(f)


def generate_image(latent_vector):
    generator = Generator(Gs_network, batch_size=1, randomize_noise=False)
    latent_vector = latent_vector.reshape((1, 18, 512))
    generator.set_dlatents(latent_vector)
    img_array = generator.generate_images()[0]
    img = PIL.Image.fromarray(img_array, 'RGB')
    return img.resize((256, 256))


def move_and_show(latent_vector, direction, coeffs):
    fig, ax = plt.subplots(1, len(coeffs), figsize=(15, 10), dpi=80)
    for i, coeff in tqdm(enumerate(coeffs), unit="image", total=len(coeffs)):
        new_latent_vector = latent_vector.copy()
        new_latent_vector[:8] = (latent_vector + coeff*direction)[:8]
        ax[i].imshow(generate_image(new_latent_vector))
        ax[i].set_title('Coeff: %0.1f' % coeff)
    [x.axis('off') for x in ax]
    plt.show()


def change_face(image="maface_01", direction="gender", coeffs=None):

    if coeffs is None:
        coeffs = [-2, 0, 2]

    directions = {
        "smile": 'ffhq_dataset/latent_directions/smile.npy',
        "gender": 'ffhq_dataset/latent_directions/gender.npy',
        "age": 'ffhq_dataset/latent_directions/age.npy'
    }
    direction = np.load(directions[direction])
    face_latent = np.load(config.latents_dir / (image + ".npy"))
    move_and_show(face_latent, direction, coeffs)


change_face()
