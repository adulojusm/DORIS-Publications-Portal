from app import db
from datetime import date


class Agency(db.Model):
    __tablename__ = 'agencies'
    aid = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    agency = db.Column(db.Enum(
        'Aging',
        'Buildings',
        'Campaign Finance',
        'Children\'s Services',
        'City Council',
        'City Clerk',
        'City Planning',
        'Citywide Admin Svcs',
        'Civilian Complaint',
        'Comm - Police Corr',
        'Community Assistance',
        'Comptroller',
        'Conflicts of Interest',
        'Consumer Affairs',
        'Contracts',
        'Correction',
        'Criminal Justice Coordinator',
        'Cultural Affairs',
        'DOI - Investigation',
        'Design/Construction',
        'Disabilities',
        'District Atty, NY County',
        'Districting Commission',
        'Domestic Violence',
        'Economic Development',
        'Education, Dept. of',
        'Elections, Board of',
        'Emergency Mgmt.',
        'Employment',
        'Empowerment Zone',
        'Environmental - DEP',
        'Environmental - OEC',
        'Environmental - ECB',
        'Equal Employment',
        'Film/Theatre',
        'Finance',
        'Fire',
        'FISA',
        'Health and Mental Hyg.',
        'HealthStat',
        'Homeless Services',
        'Hospitals - HHC',
        'Housing - HPD',
        'Human Rights',
        'Human Rsrcs - HRA',
        'Immigrant Affairs',
        'Independent Budget',
        'Info. Tech. and Telecom.',
        'Intergovernmental',
        'International Affairs',
        'Judiciary Committee',
        'Juvenile Justice',
        'Labor Relations',
        'Landmarks',
        'Law Department',
        'Library - Brooklyn',
        'Library - New York',
        'Library - Queens',
        'Loft Board',
        'Management and Budget',
        'Mayor',
        'Metropolitan Transportation Authority',
        'NYCERS',
        'Operations',
        'Parks and Recreation',
        'Payroll Administration',
        'Police',
        'Police Pension Fund',
        'Probation',
        'Public Advocate',
        'Public Health',
        'Public Housing-NYCHA',
        'Records',
        'Rent Guidelines',
        'Sanitation',
        'School Construction',
        'Small Business Svcs',
        'Sports Commission',
        'Standards and Appeal',
        'Tax Appeals Tribunal',
        'Tax Commission',
        'Taxi and Limousine',
        'Transportation',
        'Trials and Hearings',
        'Veterans - Military',
        'Volunteer Center',
        'Voter Assistance',
        'Youth & Community'), nullable=False, index=True)
    documents = db.relationship('Document', backref='agency', lazy='dynamic')

    def __repr__(self):
        return '<Agency %r>' % self.agency


class Category(db.Model):
    __tablename__ = 'categories'
    cid = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    category = db.Column(db.Enum(
        'Business and Consumers',
        'Cultural/Entertainment',
        'Education',
        'Environment',
        'Finance and Budget',
        'Government Policy',
        'Health',
        'Housing and Buildings',
        'Human Services',
        'Labor Relations',
        'Public Safety',
        'Recreation/Parks',
        'Sanitation',
        'Technology',
        'Transportation'), nullable=False, index=True)
    documents = db.relationship('Document', backref='category', lazy='dynamic')

    def __repr__(self):
        return '<Category %r>' % self.category


class Type(db.Model):
    __tablename__ = 'types'
    tid = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    type = db.Column(db.Enum(
        'Annual Report',
        'Audit Report',
        'Bond Offering - Official Statements',
        'Budget Report',
        'Consultant Report',
        'Guide - Manual',
        'Hearing - Minutes',
        'Legislative Document',
        'Memoranda - Directive',
        'Press Release',
        'Serial Publication',
        'Staff Report',
        'Report'), nullable=False, index=True)
    documents = db.relationship('Document', backref='type', lazy='dynamic')

    def __repr__(self):
        return '<Type %r>' % self.type


class Document(db.Model):
    __tablename__ = 'Documents'
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    title = db.Column(db.String(10000), index=True, nullable=False)
    description = db.Column(db.String(10000), index=True, nullable=False)
    date_created = db.Column(db.Date, nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    commonid = db.Column(db.Integer, default=None)
    sectionid = db.Column(db.Integer, default=None)
    num_access = db.Column(db.Integer, nullable=False, default=0)
    aid = db.Column(db.Integer, db.ForeignKey('agencies.aid'))
    cid = db.Column(db.Integer, db.ForeignKey('categories.cid'))
    tid = db.Column(db.Integer, db.ForeignKey('types.tid'))

    def __repr__(self):
        return '<Document %r>' % self.title

#d1 = models.Document(title="hello",description="yo",date_created=ex,filename="file",num_access=0)




