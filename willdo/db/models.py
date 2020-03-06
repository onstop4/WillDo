from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Date, Table


Base = declarative_base()

class AvailableTasklist(Base):
    __tablename__ = 'tasklists'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    tasks = relationship('IndividualTask', back_populates='tasklist', cascade='all')

    def __repr__(self):
        return "<AvailableTasklist(name='{name}')>".format(name=self.name)
    
    def delete_orphan_tags(self, session):
        for task in self.tasks:
            task.delete_orphan_tags()


tagged_tasks = Table('tagged_tasks', Base.metadata,
    Column('task_id', ForeignKey('tasks.id'), primary_key=True),
    Column('tag_id', ForeignKey('tags.id'), primary_key=True)
)


class IndividualTask(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    tasklist_id = Column(Integer, ForeignKey('tasklists.id'))
    tasklist = relationship('AvailableTasklist', back_populates='tasks', cascade='all')

    is_complete = Column(Boolean, default=False, nullable=False)
    priority = Column(String, nullable=True)
    completion_date = Column(Date, nullable=True)
    creation_date = Column(Date, nullable=True)
    description = Column(String, nullable=False)
    
    tags = relationship('Tag', secondary='tagged_tasks', back_populates='tasks', cascade='all')

    def __repr__(self):
        return "<IndividualTask(tasklist_id='{id}', description='{description}')>".format(id=self.tasklist_id, description=self.description)

    def delete_orphan_tags(self, session):
        for tag in self.tags:
            tag.delete_if_orphan()


class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    keyword = Column(String, nullable=False, unique=True)

    tasks = relationship('IndividualTask', secondary='tagged_tasks', back_populates='tags', cascade='all')

    def __repr__(self):
        return "<Tag(keyword='{keyword}')>".format(keyword=self.keyword)

    def delete_if_orphan(self, session):
        if len(self.tasks) == 0:
            session.delete(self)
            return True
        return False
