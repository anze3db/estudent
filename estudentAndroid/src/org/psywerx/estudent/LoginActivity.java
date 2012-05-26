package org.psywerx.estudent;

import org.psywerx.estudent.json.User;

import android.app.Activity;
import android.app.ProgressDialog;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

public class LoginActivity extends Activity implements ResponseListener{

	private EditText mEditUsername;
	private EditText mEditPassword;
	private Button mBtnConfirm;
	private ResponseListener mListener;
	private ProgressDialog mProgressDialog = null;

	@Override
	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.login_layout);
		init();
	}

	private void init() {
		mListener = this;
		mEditUsername = (EditText) findViewById(R.id.eUsername);
		mEditPassword = (EditText) findViewById(R.id.ePassword);
		mBtnConfirm = (Button) findViewById(R.id.btnConfirm);
		mBtnConfirm.requestFocus();
		setListeners();
	}

	private void setListeners(){
		mBtnConfirm.setOnClickListener(new View.OnClickListener() {
			public void onClick(View v) {
				String username = mEditUsername.getText().toString();
				String password = mEditPassword.getText().toString();
				if (username.equals(getString(R.string.edit_text_username)) || 
						mEditUsername.length() == 0 ) {
					mEditUsername.setError(getText(R.string.error_required));
					return;
				}
				if (password.equals(getString(R.string.edit_text_password)) ||
						mEditPassword.length() == 0 ) {
					mEditPassword.setError(getText(R.string.error_required));
					return;
				}
				mProgressDialog = ProgressDialog.show(LoginActivity.this,    
						"Please wait...", "Retrieving data ...", true);
				Api.loginRequest(mListener, username, password);
			}
		});
	}

	@Override
	protected void onResume() {
		super.onResume();
	}
	
	public void onServerResponse(Object o) {
		mProgressDialog.dismiss();
		if (o != null && o instanceof User){
			User user = (User) o;
			if (user.getLogin()){
				Intent intent = new Intent(this, MenuActivity.class);
			    Bundle bundle = new Bundle();
			    bundle.putString("firstname", user.getName());
			    bundle.putString("lastname", user.getSurname());
			    bundle.putString("username", mEditUsername.getText().toString());
			    bundle.putString("password", mEditPassword.getText().toString());
			    intent.putExtras(bundle);
				startActivity(intent);
			}else{
				Toast.makeText(this, user.getErrors(), 2000).show();
			}
		}
	}
}
