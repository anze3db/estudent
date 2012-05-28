package org.psywerx.estudent;

import org.psywerx.estudent.api.Api;
import org.psywerx.estudent.api.ResponseListener;
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
	private ProgressDialog mProgressDialog = null;
	private ResponseListener mListener;
	
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.login_layout);
        
        init();
        setListeners();
    }
    
	private void init() {
		mListener = (ResponseListener) this;
		mEditUsername = (EditText) findViewById(R.id.eUsername);
		mEditPassword = (EditText) findViewById(R.id.ePassword);
		mBtnConfirm = (Button) findViewById(R.id.btnConfirm);
	}
	
	private void setListeners(){
		mBtnConfirm.setOnClickListener(new View.OnClickListener() {
			public void onClick(View v) {
				String username = mEditUsername.getText().toString();
				String password = mEditPassword.getText().toString();
				if (username.length() == 0) {
					mEditUsername.setError(getText(R.string.error_required));
					mEditUsername.requestFocus();
					return;
				}
				if (password.length() == 0) {
					mEditPassword.setError(getText(R.string.error_required));
					mEditPassword.requestFocus();
					return;
				}
				mProgressDialog = ProgressDialog.show(LoginActivity.this,    
						getString(R.string.loading_please_wait), 
						getString(R.string.loading_verifying_login), true);
				Api.loginRequest(mListener, username, password);
			}
		});
	}
	
	@Override
	protected void onResume() {
		super.onResume();
		mEditUsername.setText("");
		mEditUsername.requestFocus();
		mEditPassword.setText("");
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
		}else{
			Toast.makeText(this, getString(R.string.communication_error), 2000).show();
		}
	}
}