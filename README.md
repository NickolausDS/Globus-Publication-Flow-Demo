# Publication Demo Portal

A Django Globus Portal Framework with a simple flow for ingesting new records

### Development

Create your environment and install packages:

```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
```

And run the portal with:

```
python manage.py runserver
```

### Creating a new search index

You will need to create a new search index in order to ingest records into it.
You can do so with the following command:

    globus search index create gdss "A search index for gdss" 

And then adding the UUID to the `app.py` file.