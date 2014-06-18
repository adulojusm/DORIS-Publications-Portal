from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Agency(db.Model):
    __tablename__ = 'agency'
    aid = db.Column(db.Integer,primary_key=True)
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


    def __init__(self, agency):
        self.agency = agency


class Category(db.Model):
    __tablename__ = 'category'
    cid = db.Column(db.Integer,primary_key=True)
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



    def __init__(self, category):
        self.category = category

class Type(db.Model):
    __tablename__ = 'type'
    tid = db.Column(db.Integer,primary_key=True)
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


    def __init__(self, type):
        self.type = type

class Document(db.Model):
    __tablename__ = 'document'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(10000), nullable=False)
    description = db.Column(db.String(10000), nullable=False)
    datecreated = db.Column(db.Date, nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    common_id = db.Column(db.Integer, default=None)
    section_id = db.Column(db.Integer, default=None)
    num_access = db.Column(db.Integer, default=0, nullable=False)
    aid = db.Column(db.Integer, db.ForeignKey('agency.aid'))

    agency = db.relationship('Agency',primaryjoin= 'Document.aid == Agency.aid', backref=db.backref('document', lazy='dynamic'))
    cid = db.Column(db.Integer, db.ForeignKey('category.cid'))

    category = db.relationship('Category', primaryjoin= 'Document.cid == Category.cid',backref=db.backref('document', lazy='dynamic'))
    tid = db.Column(db.Integer, db.ForeignKey('type.tid'))
    type = db.relationship('Type',primaryjoin= 'Document.tid == Type.tid', backref=db.backref('document', lazy='dynamic'))
    url = db.Column(db.String(255), nullable=False)
    puborfoil = db.Column(db.Enum('Publication','FOIL'),nullable=False)

    def __init__(self, title, description, datecreated, filename, num_access, url, puborfoil):
        self.title=title
        self.description = description
        self.datecreated = datecreated
        self.filename = filename
        self.num_access = num_access
        self.url = url
        self.puborfoil = puborfoil