#!/usr/bin/env python

from cupsAccounting.job import Job
from cupsAccounting.utiles import objetoBase
from cupsAccounting.logger import Logger


class Queue(objetoBase, Logger):

    def __init__(self, c, name):
        self.c = c
        self.name = name
        self.uri = self.attr['printer-uri-supported'][0]

    @property
    def attr(self):
        return self.c.getPrinterAttributes(self.name)

    @property
    def jobs(self):
        jobs = []
        for jid in self.c.getJobs().keys():
            if self.c.getJobAttributes(jid)['job-printer-uri'] == self.uri:
                jobs.append(Job(self.c, jid))
        return jobs

    @property
    def empty(self):
        if len(self.jobs) == 0:
            return True
        return False

    def status(self):
        status = "%s" % self
        for j in self.jobs:
            status += "\n\t\t%s" % j
        return status


    def __repr__(self):
        return """{clase} {name} ({n} jobs)""".format(
            clase=self.__class__.__name__,
            name=self.name,
            n=len(self.jobs),
            )
