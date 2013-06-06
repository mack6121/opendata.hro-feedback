# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Vorschlag'
        db.create_table('opendata_vorschlag_vorschlag', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=128)),
            ('betreff', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('beschreibung', self.gf('django.db.models.fields.TextField')(max_length=4096)),
            ('freigegeben', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('erstellt_datum', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('opendata_vorschlag', ['Vorschlag'])

        # Adding model 'VorschlagStatus'
        db.create_table('opendata_vorschlag_vorschlagstatus', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('vorschlag', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['opendata_vorschlag.Vorschlag'])),
            ('details', self.gf('django.db.models.fields.TextField')()),
            ('status', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('erstellt_datum', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('opendata_vorschlag', ['VorschlagStatus'])


    def backwards(self, orm):
        # Deleting model 'Vorschlag'
        db.delete_table('opendata_vorschlag_vorschlag')

        # Deleting model 'VorschlagStatus'
        db.delete_table('opendata_vorschlag_vorschlagstatus')


    models = {
        'opendata_vorschlag.vorschlag': {
            'Meta': {'ordering': "['-erstellt_datum']", 'object_name': 'Vorschlag'},
            'beschreibung': ('django.db.models.fields.TextField', [], {'max_length': '4096'}),
            'betreff': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '128'}),
            'erstellt_datum': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'freigegeben': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'opendata_vorschlag.vorschlagstatus': {
            'Meta': {'ordering': "['vorschlag', '-erstellt_datum']", 'object_name': 'VorschlagStatus'},
            'details': ('django.db.models.fields.TextField', [], {}),
            'erstellt_datum': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'vorschlag': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['opendata_vorschlag.Vorschlag']"})
        }
    }

    complete_apps = ['opendata_vorschlag']