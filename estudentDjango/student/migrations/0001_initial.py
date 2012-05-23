# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Student'
        db.create_table('student_student', (
            ('enrollment_number', self.gf('django.db.models.fields.IntegerField')(default=63110003, unique=True, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('surname', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('social_security_number', self.gf('django.db.models.fields.CharField')(max_length=13, null=True, blank=True)),
            ('tax_number', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=255)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('birth_date', self.gf('django.db.models.fields.DateField')()),
            ('birth_country', self.gf('django.db.models.fields.related.ForeignKey')(related_name='birth_country', to=orm['codelist.Country'])),
            ('birth_place', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('birth_region', self.gf('django.db.models.fields.related.ForeignKey')(related_name='region', to=orm['codelist.Region'])),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
        ))
        db.send_create_signal('student', ['Student'])

        # Adding model 'Address'
        db.create_table('student_address', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('street', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('region', self.gf('django.db.models.fields.related.ForeignKey')(related_name='address_region', to=orm['codelist.Region'])),
            ('post', self.gf('django.db.models.fields.related.ForeignKey')(related_name='address_post', to=orm['codelist.Post'])),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(related_name='address_country', to=orm['codelist.Country'])),
            ('student', self.gf('django.db.models.fields.related.ForeignKey')(related_name='student', to=orm['student.Student'])),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('send_address', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('student', ['Address'])

        # Adding model 'Enrollment'
        db.create_table('student_enrollment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('student', self.gf('django.db.models.fields.related.ForeignKey')(related_name='enrollment_student', to=orm['student.Student'])),
            ('program', self.gf('django.db.models.fields.related.ForeignKey')(related_name='study_program', to=orm['codelist.StudyProgram'])),
            ('study_year', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('class_year', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('enrol_type', self.gf('django.db.models.fields.CharField')(default='V1', max_length=2)),
        ))
        db.send_create_signal('student', ['Enrollment'])

        # Adding unique constraint on 'Enrollment', fields ['student', 'study_year', 'program', 'class_year']
        db.create_unique('student_enrollment', ['student_id', 'study_year', 'program_id', 'class_year'])

        # Adding M2M table for field courses on 'Enrollment'
        db.create_table('student_enrollment_courses', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('enrollment', models.ForeignKey(orm['student.enrollment'], null=False)),
            ('course', models.ForeignKey(orm['codelist.course'], null=False))
        ))
        db.create_unique('student_enrollment_courses', ['enrollment_id', 'course_id'])

        # Adding M2M table for field modules on 'Enrollment'
        db.create_table('student_enrollment_modules', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('enrollment', models.ForeignKey(orm['student.enrollment'], null=False)),
            ('module', models.ForeignKey(orm['student.module'], null=False))
        ))
        db.create_unique('student_enrollment_modules', ['enrollment_id', 'module_id'])

        # Adding model 'ExamDate'
        db.create_table('student_examdate', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(related_name='course', to=orm['codelist.Course'])),
            ('instructor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['codelist.Instructor'])),
            ('study_year', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=7)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('nr_SignUp', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('total_points', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('min_pos', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('allowed', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['student.StudentsGroup'])),
        ))
        db.send_create_signal('student', ['ExamDate'])

        # Adding model 'ExamSignUp'
        db.create_table('student_examsignup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('enroll', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['student.Enrollment'])),
            ('examDate', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['student.ExamDate'])),
            ('VP', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('result_exam', self.gf('django.db.models.fields.CharField')(default='NR', max_length=2)),
            ('result_practice', self.gf('django.db.models.fields.CharField')(default='NR', max_length=2)),
            ('points', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('paidfor', self.gf('django.db.models.fields.CharField')(default='Y', max_length=2)),
            ('valid', self.gf('django.db.models.fields.CharField')(default='Y', max_length=2)),
        ))
        db.send_create_signal('student', ['ExamSignUp'])

        # Adding model 'Module'
        db.create_table('student_module', (
            ('module_code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=6, primary_key=True)),
            ('descriptor', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('student', ['Module'])

        # Adding model 'Curriculum'
        db.create_table('student_curriculum', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['codelist.Course'])),
            ('program', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['codelist.StudyProgram'])),
            ('class_year', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('mandatory', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('valid', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('module', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['student.Module'], null=True, blank=True)),
            ('only_exam', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('student', ['Curriculum'])

        # Adding model 'StudentsGroup'
        db.create_table('student_studentsgroup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('canSignUp', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('student', ['StudentsGroup'])

        # Adding M2M table for field student on 'StudentsGroup'
        db.create_table('student_studentsgroup_student', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('studentsgroup', models.ForeignKey(orm['student.studentsgroup'], null=False)),
            ('student', models.ForeignKey(orm['student.student'], null=False))
        ))
        db.create_unique('student_studentsgroup_student', ['studentsgroup_id', 'student_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Enrollment', fields ['student', 'study_year', 'program', 'class_year']
        db.delete_unique('student_enrollment', ['student_id', 'study_year', 'program_id', 'class_year'])

        # Deleting model 'Student'
        db.delete_table('student_student')

        # Deleting model 'Address'
        db.delete_table('student_address')

        # Deleting model 'Enrollment'
        db.delete_table('student_enrollment')

        # Removing M2M table for field courses on 'Enrollment'
        db.delete_table('student_enrollment_courses')

        # Removing M2M table for field modules on 'Enrollment'
        db.delete_table('student_enrollment_modules')

        # Deleting model 'ExamDate'
        db.delete_table('student_examdate')

        # Deleting model 'ExamSignUp'
        db.delete_table('student_examsignup')

        # Deleting model 'Module'
        db.delete_table('student_module')

        # Deleting model 'Curriculum'
        db.delete_table('student_curriculum')

        # Deleting model 'StudentsGroup'
        db.delete_table('student_studentsgroup')

        # Removing M2M table for field student on 'StudentsGroup'
        db.delete_table('student_studentsgroup_student')


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