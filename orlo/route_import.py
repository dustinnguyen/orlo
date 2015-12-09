from __future__ import print_function
import arrow
from flask import jsonify, request
from orlo import app
from orlo.orm import db, Package, Release, PackageResult, ReleaseNote, Platform
from orlo.views import _validate_request_json
from orlo.util import list_to_string
from sqlalchemy.orm import exc


__author__ = 'alforbes'


@app.route('/import', methods=['GET'])
@app.route('/import/release', methods=['GET'])
def get_import():
    """
    Display a useful message on how to import

    :status 200:
    """

    msg = 'This is the orlo import url'
    return jsonify(message=msg), 200


@app.route('/releases/import', methods=['POST'])
def post_import():
    """
    Import a release

    The document must contain a list of full releases, example:
    [
        {
            'ftime': '2015-11-18T19:21:12Z',
            'notes': ['note1', 'note2'],
            'packages': [
                {
                    'diff_url': None,
                    'ftime': '2015-11-18T19:21:12Z',
                    'name': 'test-package',
                    'rollback': 'false',
                    'status': 'SUCCESSFUL',
                    'stime': '2015-11-18T19:21:12Z',
                    'version': '1.2.3',
                }
            ],
            'platforms': ['test_platform'],
            'references': ['TestTicket-123'],
            'stime': '2015-11-18T19:21:12Z',
            'team': 'test team',
            'user': 'testuser'
        },
        {...}
    ]

    :status 200: The document was accepted
    """

    _validate_request_json(request)

    releases = []
    for r in request.json:
        # Get the platform, create if it doesn't exist
        platforms = []
        for p in r['platforms']:
            try:
                query = db.session.query(Platform).filter(Platform.name == p)
                platform = query.one()
            except exc.NoResultFound:
                app.logger.info("Creating platform {}".format(p))
                platform = Platform(p)
                db.session.add(platform)
            platforms.append(platform)

        release = Release(
            platforms=platforms,
            user=r['user'],
            team=r['team'],
            references=r['references'],
        )

        release.ftime = arrow.get(r['ftime'])
        release.stime = arrow.get(r['stime'])
        release.duration = release.ftime - release.stime

        try:
            notes = r['notes']
            for n in notes:
                note = ReleaseNote(release.id, n)
                db.session.add(note)
        except KeyError:
            pass

        for p in r['packages']:
            package = Package(
                release_id=release.id,
                name=p['name'],
                version=p['version'],
            )
            package.stime = arrow.get(p['stime'])
            package.ftime = arrow.get(p['ftime'])
            package.duration = package.ftime - package.stime
            package.rollback = p['rollback']
            package.status = p['status']
            package.diff_url = p['diff_url']

            db.session.add(package)

        db.session.add(release)
        db.session.commit()

        releases.append(release.id)

    return jsonify({'releases': [str(x) for x in releases]}), 200
