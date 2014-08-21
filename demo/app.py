#!/usr/bin/env python3
import argparse
import os

import service

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Face recognizing service.")
    parser.add_argument("-g", "--gallery_path", default="./gallery/star_face_gallery",
                        help="gallery file")
    parser.add_argument("-m", "--model_path", default="./models",
                        help="model file")
    args = parser.parse_args()

    fd_instance = service.fd_create_instance()

    fr_instance = service.fr_create_instance(args.model_path)
    if not os.path.isfile(args.gallery_path):
        service.fr_create_new_gallery(args.gallery_path)
    service.fr_load_faces(fr_instance, args.gallery_path)

    # do something

    service.fd_destroy_instance(fd_instance)
    service.fr_destroy_instance(fr_instance)
