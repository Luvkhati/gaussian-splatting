import os
import argparse
import shutil
import numpy as np
from scene.colmap_loader import read_colmap_scene

def write_cam_file(filepath, cam_matrix, w, h):
    with open(filepath, "w") as f:
        f.write(f"{w} {h}\n")
        for row in cam_matrix:
            f.write(" ".join(str(val) for val in row) + "\n")

def convert_colmap(input_path, output_path, images_dir="images"):
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # Load COLMAP data
    scene = read_colmap_scene(
        path=input_path,
        images_dir=images_dir,
        max_num_imgs=-1
    )

    # Save camera poses
    for idx, img in enumerate(scene.train_cameras):
        cam_matrix = img.colmap_to_opengl()
        out_path = os.path.join(output_path, f"{idx:05d}.txt")
        write_cam_file(out_path, cam_matrix, img.image.width, img.image.height)

    # Save intrinsics
    fx = scene.train_cameras[0].fx
    fy = scene.train_cameras[0].fy
    cx = scene.train_cameras[0].cx
    cy = scene.train_cameras[0].cy
    w = scene.train_cameras[0].image.width
    h = scene.train_cameras[0].image.height
    with open(os.path.join(output_path, "intrinsics.txt"), "w") as f:
        f.write(f"{fx} {fy} {cx} {cy} {w} {h}\n")

    # Copy images
    image_out_path = os.path.join(output_path, "images")
    if not os.path.exists(image_out_path):
        os.makedirs(image_out_path)

    for img in scene.train_cameras:
        src = os.path.join(input_path, images_dir, img.image_name)
        dst = os.path.join(image_out_path, img.image_name)
        shutil.copyfile(src, dst)

    print("✅ COLMAP conversion complete!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_path", type=str, required=True)
    parser.add_argument("--output_path", type=str, required=True)
    parser.add_argument("--images", type=str, default="images")
    args = parser.parse_args()

    convert_colmap(args.input_path, args.output_path, args.images)
