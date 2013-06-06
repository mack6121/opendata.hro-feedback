# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'VorschlagStatus.mitgeteilt'
        db.add_column('opendata_vorschlag_vorschlagstatus', 'mitgeteilt',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'VorschlagStatus.mitgeteilt'
        db.delete_column('opendata_vorschlag_vorschlagstatus', 'mitgeteilt')


    models = {
        'opendata_vorschlag.vorschlag': {
            'Meta': {'ordering': "['-erstellt_datum']", 'object_name': 'Vorschlag'},
            'beschreibung': ('django.db.models.fields.TextField', [], {'max_length': '4096'}),
            'betreff': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
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
            'mitgeteilt': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'status': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'vorschlag': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['opendata_vorschlag.Vorschlag']"})
        }
    }

    complete_apps = ['opendata_vorschlag']