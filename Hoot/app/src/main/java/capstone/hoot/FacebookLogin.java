package capstone.hoot;

import com.facebook.CallbackManager;
import com.facebook.FacebookCallback;
import com.facebook.FacebookException;
import com.facebook.FacebookSdk;
import com.facebook.login.LoginResult;
import com.facebook.login.widget.LoginButton;

import android.content.Intent;
import android.support.v4.app.FragmentActivity;
import android.os.Bundle;
import android.util.Log;

import java.util.Arrays;

public class FacebookLogin extends FragmentActivity {
    public static final String LOGTAG = "HOOTLOG";
    private CallbackManager callbackManager;
    LoginButton login_button;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        // Initialize the SDK before executing any other operations,
        // especially, if you're using Facebook UI elements.
        FacebookSdk.sdkInitialize(getApplicationContext());
        callbackManager = CallbackManager.Factory.create();

        setContentView(R.layout.login);

        login_button = (LoginButton) findViewById(R.id.login_button);

        // Set facebook permissions to view profile info, email, and friends of the logged in user
        login_button.setReadPermissions(Arrays.asList("public_profile", "email", "user_friends"));

        // Callback registration
        login_button.registerCallback(callbackManager, new FacebookCallback<LoginResult>() {
            @Override
            public void onSuccess(LoginResult loginResult) {
                // App code
                Log.d(LOGTAG, "SUCCESSFULLY LOGGED IN");
                // from here we want to launch a new intent
                // that launches a new activity (probably bookshelf view_
            }

            @Override
            public void onCancel() {
                Log.d(LOGTAG, "CANCELLED LOG IN");
                // we probably dont want to do anything, just return to the
            }

            @Override
            public void onError(FacebookException exception) {
                // App code
                Log.d(LOGTAG, "FACEBOOK ERROR");
            }
        });
    }

    /**
     * The Activty returning results is the Facebook login activity
     * We simply take the data being returned to Android's onActivityResult
     * and send it to the callbackManager's onActivityResult method;
     * @param requestCode
     * @param resultCode
     * @param data
     */
    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        callbackManager.onActivityResult(requestCode, resultCode, data);
    }
}
