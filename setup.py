from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="AdaptiveDrone",
    version="0.1.0",
    author="Abumere, Himadri, Tejas, Daniel",
    author_email="Abumere_Okhihan@student.uml.edu",
    description="Drone app with face gesture and GUI control",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Abumere17/AdaptiveDrone",
    packages=find_packages(include=[
        "AppMainAndGUI",
        "FaceDetectionModule",
        "TelloControlModule"
    ]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "djitellopy",
        "opencv-python",
        "mediapipe",
        "tk",
        "numpy"
    ],
    entry_points={
        "console_scripts": [
            "adaptive-drone=AppMainAndGUI.MainMenu:main"
        ]
    }
)
