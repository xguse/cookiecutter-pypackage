{% set is_open_source = cookiecutter.open_source_license != 'Not open source' -%}
{% for _ in cookiecutter.project_name %}={% endfor %}
{{ cookiecutter.project_name }}
{% for _ in cookiecutter.project_name %}={% endfor %}

{% if is_open_source %}
.. image:: https://img.shields.io/pypi/v/{{ cookiecutter.project_slug }}.svg
        :target: https://pypi.python.org/pypi/{{ cookiecutter.project_slug }}

.. image:: https://img.shields.io/travis/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}.svg
        :target: https://travis-ci.org/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}

.. image:: https://readthedocs.org/projects/{{ cookiecutter.project_slug | replace("_", "-") }}/badge/?version=latest
        :target: https://{{ cookiecutter.project_slug | replace("_", "-") }}.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status
{%- endif %}

.. image:: https://pyup.io/repos/github/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/shield.svg
     :target: https://pyup.io/repos/github/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/
     :alt: Updates


{{ cookiecutter.project_short_description }}

{% if is_open_source %}
* Free software: {{ cookiecutter.open_source_license }}
* Documentation: https://{{ cookiecutter.project_slug | replace("_", "-") }}.readthedocs.io.
{% endif %}

Features
--------

* TODO

Install for Development
-----------------------

#. Install and become familiar with `conda/Anaconda <https://conda.io/docs/user-guide/install/index.html>`_.
#. Fork the repository to your github by clicking `here <https://github.com/xguse/table_enforcer#fork-destination-box>`_.
#. Clone your forked repo to your dev computer: ``git clone git@github.com:YOUR_GITHUB_NAME/table_enforcer.git``.
#. Enter your freshly cloned {{ cookiecutter.project_name }} directory: ``cd {{ cookiecutter.project_slug }}``.
#. Run ``make help`` to see most of the ``make`` targets available.
#. Running ``make install``. This creates and registers a ``conda`` environment named {{ cookiecutter.project_slug }}. Into that conda environment, it installs all of the needed libraries to run and develop {{ cookiecutter.project_name }}.
#. To uninstall your dev environment just run ``make uninstall-conda-env``. All traces of the environment should be erased.
#. Remember to activate the ``conda`` env before you try to use or interact with {{ cookiecutter.project_name }} or you will not have access to it.

Credits
---------

This package was created with Cookiecutter_ and the `xguse/cookiecutter-pypackage`_ project template which is based on `audreyr/cookiecutter-pypackage`_.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _`xguse/cookiecutter-pypackage`: https://github.com/xguse/cookiecutter-pypackage

