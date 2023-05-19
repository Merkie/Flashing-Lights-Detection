# Flashing Lights Detection

Flashing Lights Detection is an open-source Python project that uses Python, OpenCV 2, and Numpy to scan videos for flashing lights. It returns an array of start and end timestamps for sections in a video which contain flashing lights. Hosted via Flask, it is designed to process the average HD video in only a few seconds asynchronously. This service is intended to be integrated into platforms that require user uploads to be vetted for safety.

## Requirements

* Python
* OpenCV 2
* Numpy
* Flask

## Installation

Before you start, ensure you have Python 3.6 or higher installed. You can check your Python version with the following command:

```
python --version
```

1. Clone this repository.

```
git clone https://github.com/Merkie/Flashing-Lights-Detection.git
```

2. Navigate into the project directory.

```
cd Flashing-Lights-Detection
```

3. Install the required Python libraries. 

```
pip install -r requirements.txt
```

## Running the Application

1. To start the server, run:

```
python app.py
```

2. By default, the server runs on `http://localhost:5000`.

## Using the Service

The service accepts video uploads via a POST request to the `/upload` endpoint.

Look at the index.html file for an example request, or launch it in your browser while the server is running for a basic user interface.

## License

Flashing Lights Detection is open-source software licensed under the MIT license.

## Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for more information.

## Support

If you encounter any issues or have any questions, please open an issue in this repository.
