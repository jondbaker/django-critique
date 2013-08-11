# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Critique'
        db.create_table(u'critique_critique', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('message', self.gf('django.db.models.fields.TextField')()),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('user_agent', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal(u'critique', ['Critique'])


    def backwards(self, orm):
        # Deleting model 'Critique'
        db.delete_table(u'critique_critique')


    models = {
        u'critique.critique': {
            'Meta': {'ordering': "['-created']", 'object_name': 'Critique'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'user_agent': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        }
    }

    complete_apps = ['critique']