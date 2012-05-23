# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Course'
        db.create_table('codelist_course', (
            ('course_code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=5, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('valid', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('codelist', ['Course'])

        # Adding M2M table for field instructors on 'Course'
        db.create_table('codelist_course_instructors', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('course', models.ForeignKey(orm['codelist.course'], null=False)),
            ('groupinstructors', models.ForeignKey(orm['codelist.groupinstructors'], null=False))
        ))
        db.create_unique('codelist_course_instructors', ['course_id', 'groupinstructors_id'])

        # Adding model 'Country'
        db.create_table('codelist_country', (
            ('category_code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=3, primary_key=True)),
            ('descriptor', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('descriptor_english', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('valid', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('codelist', ['Country'])

        # Adding model 'StudyProgram'
        db.create_table('codelist_studyprogram', (
            ('program_code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=5, primary_key=True)),
            ('descriptor', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('valid', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('codelist', ['StudyProgram'])

        # Adding model 'Post'
        db.create_table('codelist_post', (
            ('post_code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=5, primary_key=True)),
            ('descriptor', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('valid', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('codelist', ['Post'])

        # Adding model 'Region'
        db.create_table('codelist_region', (
            ('region_code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=3, primary_key=True)),
            ('descriptor', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('valid', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('codelist', ['Region'])

        # Adding model 'Faculty'
        db.create_table('codelist_faculty', (
            ('faculty_code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=3, primary_key=True)),
            ('descriptor', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('valid', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('codelist', ['Faculty'])

        # Adding model 'Instructor'
        db.create_table('codelist_instructor', (
            ('instructor_code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=6, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('surname', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('valid', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, null=True)),
        ))
        db.send_create_signal('codelist', ['Instructor'])

        # Adding model 'GroupInstructors'
        db.create_table('codelist_groupinstructors', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('codelist', ['GroupInstructors'])

        # Adding M2M table for field instructor on 'GroupInstructors'
        db.create_table('codelist_groupinstructors_instructor', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('groupinstructors', models.ForeignKey(orm['codelist.groupinstructors'], null=False)),
            ('instructor', models.ForeignKey(orm['codelist.instructor'], null=False))
        ))
        db.create_unique('codelist_groupinstructors_instructor', ['groupinstructors_id', 'instructor_id'])


    def backwards(self, orm):
        # Deleting model 'Course'
        db.delete_table('codelist_course')

        # Removing M2M table for field instructors on 'Course'
        db.delete_table('codelist_course_instructors')

        # Deleting model 'Country'
        db.delete_table('codelist_country')

        # Deleting model 'StudyProgram'
        db.delete_table('codelist_studyprogram')

        # Deleting model 'Post'
        db.delete_table('codelist_post')

        # Deleting model 'Region'
        db.delete_table('codelist_region')

        # Deleting model 'Faculty'
        db.delete_table('codelist_faculty')

        # Deleting model 'Instructor'
        db.delete_table('codelist_instructor')

        # Deleting model 'GroupInstructors'
        db.delete_table('codelist_groupinstructors')

        # Removing M2M table for field instructor on 'GroupInstructors'
        db.delete_table('codelist_groupinstructors_instructor')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'codelist.country': {
            'Meta': {'object_name': 'Country'},
            'category_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '3', 'primary_key': 'True'}),
            'descriptor': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'descriptor_english': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'valid': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'codelist.course': {
            'Meta': {'object_name': 'Course'},
            'course_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '5', 'primary_key': 'True'}),
            'instructors': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['codelist.GroupInstructors']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'program': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['codelist.StudyProgram']", 'symmetrical': 'False', 'through': "orm['student.Curriculum']", 'blank': 'True'}),
            'valid': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'codelist.faculty': {
            'Meta': {'object_name': 'Faculty'},
            'descriptor': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'faculty_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '3', 'primary_key': 'True'}),
            'valid': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'codelist.groupinstructors': {
            'Meta': {'object_name': 'GroupInstructors'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instructor': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['codelist.Instructor']", 'null': 'True', 'blank': 'True'})
        },
        'codelist.instructor': {
            'Meta': {'object_name': 'Instructor'},
            'instructor_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '6', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'null': 'True'}),
            'valid': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'codelist.post': {
            'Meta': {'object_name': 'Post'},
            'descriptor': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'post_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '5', 'primary_key': 'True'}),
            'valid': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'codelist.region': {
            'Meta': {'object_name': 'Region'},
            'descriptor': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'region_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '3', 'primary_key': 'True'}),
            'valid': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'codelist.studyprogram': {
            'Meta': {'object_name': 'StudyProgram'},
            'descriptor': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'program_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '5', 'primary_key': 'True'}),
            'valid': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'student.curriculum': {
            'Meta': {'ordering': "['program']", 'object_name': 'Curriculum'},
            'class_year': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['codelist.Course']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mandatory': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'module': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['student.Module']", 'null': 'True', 'blank': 'True'}),
            'only_exam': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'program': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['codelist.StudyProgram']"}),
            'valid': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'student.module': {
            'Meta': {'object_name': 'Module'},
            'descriptor': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'module_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '6', 'primary_key': 'True'})
        }
    }

    complete_apps = ['codelist']