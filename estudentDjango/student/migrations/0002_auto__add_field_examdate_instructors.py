# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'ExamDate.instructors'
        db.add_column('student_examdate', 'instructors',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['codelist.GroupInstructors']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'ExamDate.instructors'
        db.delete_column('student_examdate', 'instructors_id')


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
        'student.address': {
            'Meta': {'object_name': 'Address'},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'address_country'", 'to': "orm['codelist.Country']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'address_post'", 'to': "orm['codelist.Post']"}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'address_region'", 'to': "orm['codelist.Region']"}),
            'send_address': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'student'", 'to': "orm['student.Student']"}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '1'})
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
        'student.enrollment': {
            'Meta': {'ordering': "['program', 'study_year', 'class_year']", 'unique_together': "(('student', 'study_year', 'program', 'class_year'),)", 'object_name': 'Enrollment'},
            'class_year': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'courses': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['codelist.Course']", 'null': 'True', 'blank': 'True'}),
            'enrol_type': ('django.db.models.fields.CharField', [], {'default': "'V1'", 'max_length': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modules': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['student.Module']", 'null': 'True', 'blank': 'True'}),
            'program': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'study_program'", 'to': "orm['codelist.StudyProgram']"}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'enrollment_student'", 'to': "orm['student.Student']"}),
            'study_year': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'student.examdate': {
            'Meta': {'object_name': 'ExamDate'},
            'allowed': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['student.StudentsGroup']"}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'course'", 'to': "orm['codelist.Course']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instructor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['codelist.Instructor']"}),
            'instructors': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['codelist.GroupInstructors']"}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '7'}),
            'min_pos': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'nr_SignUp': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'students': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['student.Enrollment']", 'through': "orm['student.ExamSignUp']", 'symmetrical': 'False'}),
            'study_year': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'total_points': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'student.examsignup': {
            'Meta': {'object_name': 'ExamSignUp'},
            'VP': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'enroll': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['student.Enrollment']"}),
            'examDate': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['student.ExamDate']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'paidfor': ('django.db.models.fields.CharField', [], {'default': "'Y'", 'max_length': '2'}),
            'points': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'result_exam': ('django.db.models.fields.CharField', [], {'default': "'NR'", 'max_length': '2'}),
            'result_practice': ('django.db.models.fields.CharField', [], {'default': "'NR'", 'max_length': '2'}),
            'valid': ('django.db.models.fields.CharField', [], {'default': "'Y'", 'max_length': '2'})
        },
        'student.module': {
            'Meta': {'object_name': 'Module'},
            'descriptor': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'module_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '6', 'primary_key': 'True'})
        },
        'student.student': {
            'Meta': {'object_name': 'Student'},
            'birth_country': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'birth_country'", 'to': "orm['codelist.Country']"}),
            'birth_date': ('django.db.models.fields.DateField', [], {}),
            'birth_place': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'birth_region': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'region'", 'to': "orm['codelist.Region']"}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '255'}),
            'enrollment_number': ('django.db.models.fields.IntegerField', [], {'default': '63110003', 'unique': 'True', 'primary_key': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'social_security_number': ('django.db.models.fields.CharField', [], {'max_length': '13', 'null': 'True', 'blank': 'True'}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'tax_number': ('django.db.models.fields.CharField', [], {'max_length': '8'})
        },
        'student.studentsgroup': {
            'Meta': {'object_name': 'StudentsGroup'},
            'canSignUp': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'student': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['student.Student']", 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['student']