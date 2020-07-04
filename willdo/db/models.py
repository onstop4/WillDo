from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Date


Base = declarative_base()


class AvailableTasklist(Base):
    __tablename__ = 'tasklists'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    tasks = relationship(
        'IndividualTask', back_populates='tasklist', cascade='all')

    def __repr__(self):
        return "<AvailableTasklist(name='{name}')>".format(name=self.name)


class IndividualTask(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    tasklist_id = Column(Integer, ForeignKey('tasklists.id'))
    tasklist = relationship('AvailableTasklist',
                            back_populates='tasks', cascade='all')

    is_complete = Column(Boolean, default=False, nullable=False)
    priority = Column(String, nullable=True)
    completion_date = Column(Date, nullable=True)
    creation_date = Column(Date, nullable=True)
    description = Column(String, nullable=False)

    def __repr__(self):
        return "<IndividualTask(tasklist_id='{id}', description='{description}')>".format(id=self.tasklist_id, description=self.description)
