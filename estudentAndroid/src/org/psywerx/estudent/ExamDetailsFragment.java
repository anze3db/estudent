package org.psywerx.estudent;

import java.util.HashMap;

import org.psywerx.estudent.api.Api;
import org.psywerx.estudent.api.ResponseListener;
import org.psywerx.estudent.json.Signup;

import android.app.Fragment;
import android.app.ProgressDialog;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

public class ExamDetailsFragment extends Fragment implements ResponseListener{
	
	private HashMap<Integer, EditText> data = new HashMap<Integer, EditText>(); 
	private Button btnApplyUnapply;
	private boolean signedup = false;
	
	private ProgressDialog mProgressDialog = null;
	private ResponseListener mListener;
	
	private ExamsFragment mSignListener;
	
	public void setmSignListener(ExamsFragment mSignListener) {
		this.mSignListener = mSignListener;
	}
	
	@Override
	public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
		mListener = (ResponseListener) this;
		
		View v = inflater.inflate(R.layout.exam_details_layout, null, false);
		((TextView)v.findViewById(R.id.examID).findViewById(R.id.title)).setText(getString(R.string.examID));
		((TextView)v.findViewById(R.id.examName).findViewById(R.id.title)).setText(getString(R.string.examName));
		((TextView)v.findViewById(R.id.examTeacher).findViewById(R.id.title)).setText(getString(R.string.examTeacher));
		((TextView)v.findViewById(R.id.examDate).findViewById(R.id.title)).setText(getString(R.string.examDate));
		
		data.put(R.id.examID, (EditText)v.findViewById(R.id.examID).findViewById(R.id.description));
		data.put(R.id.examName, (EditText)v.findViewById(R.id.examName).findViewById(R.id.description));
		data.put(R.id.examTeacher, (EditText)v.findViewById(R.id.examTeacher).findViewById(R.id.description));
		data.put(R.id.examDate, (EditText)v.findViewById(R.id.examDate).findViewById(R.id.description));
		
		btnApplyUnapply = (Button)v.findViewById(R.id.btnApplyUnapply);
		btnApplyUnapply.setOnClickListener(new View.OnClickListener() {
			public void onClick(View v) {
				if(signedup) {
					mProgressDialog = ProgressDialog.show(getActivity(),    
							getString(R.string.loading_please_wait), 
							getString(R.string.loading_verifying_login), true);
					Api.unapplyExam(mListener, StaticData.username, data.get(R.id.examID).getText().toString());
				} else {
					mProgressDialog = ProgressDialog.show(getActivity(),    
							getString(R.string.loading_please_wait), 
							getString(R.string.loading_verifying_login), true);
					Api.applyExam(mListener, StaticData.username, data.get(R.id.examID).getText().toString());
				}
			}
		});
		
		return v;
	}
	
	public void showData(String id, String name, String teacher, String date, boolean signedup) {
		data.get(R.id.examID).setText(id);
		data.get(R.id.examName).setText(name);
		data.get(R.id.examTeacher).setText(teacher);
		data.get(R.id.examDate).setText(date);
		this.signedup = signedup;
		if(signedup)
			btnApplyUnapply.setText(R.string.unapplyExam);
		else
			btnApplyUnapply.setText(R.string.applyExam);
	}

	public void onServerResponse(Object o) {
		mProgressDialog.dismiss();
		if (o != null && o instanceof Signup) {
			Signup e = (Signup)o;
			if(e.error.isEmpty()) {
				Toast.makeText(getActivity(), e.msg, Toast.LENGTH_LONG).show();
				if(signedup) {
					btnApplyUnapply.setText(R.string.unapplyExam);
					this.signedup = false;
					if(mSignListener != null)
						mSignListener.onSign(false);
				} else {
					btnApplyUnapply.setText(R.string.applyExam);
					this.signedup = true;
					if(mSignListener != null)
						mSignListener.onSign(true);
				}
			} else {
				Toast.makeText(getActivity(), e.error, Toast.LENGTH_LONG).show();
			}	
		}
	}
}
