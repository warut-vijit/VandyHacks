class Graph(models.Model):
    title = models.CharField(max_length=60)
    description = models.TextField(max_length=10000, blank=True, null=True)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now=True)
    

    def num_comments(self):
        return self.Comment_set.count()

    def last_post(self):
        if self.Comment_set.count():
            return self.post_set.order_by("created")[0]

    def proPercent(self):
        if self.votesfor == 0 and self.votesagainst == 0:
            return 50
        else:
            numPro = self.votesfor
            numCon = self.votesagainst
        
            total = numPro + numCon
            proP = numPro*100/total
            return proP
        
        
    def __unicode__(self):
        return unicode(self.creator) + " - " + self.title
#!/usr/bin/env python

