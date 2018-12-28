Installation Guide
==================

Installation Guide
==================
.. warning::
	Unfortunatelly, I deleted upload folder in static folder by mistake. If you want to merge this project, be sure that you created 'upload' folder in 'static' folder.
	Otherwise, you will get 'Internal Server Error' while uploding images.


To further develop this project, you can install python packages package by package or with 'requirements.txt' on itucsdb1827's GitHub page.

Run the following command to install the dependencies:

.. code-block:: console

   python -m pip install -r requirements.txt

After installation of python packages, you can open project with:

.. code-block:: console

   python3 server.py
   
But first you have to extract tables from 'mydb.sql' and change database adress on 'server.py' in line 17:

.. code-block:: console

   adress="YOUR_DATABASE_ADRESS"
