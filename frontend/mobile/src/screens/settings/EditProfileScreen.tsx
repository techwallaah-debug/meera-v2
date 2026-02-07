import React, {useState} from 'react';
import {View, StyleSheet, ScrollView, Alert, TouchableOpacity} from 'react-native';
import {
  TextInput,
  Button,
  Text,
  Card,
  Avatar,
  useTheme,
  ActivityIndicator,
} from 'react-native-paper';
import {launchImageLibrary} from 'react-native-image-picker';
import {useAuthStore} from '../../store/authStore';
import {apiService} from '../../services/api';
import {spacing, borderRadius} from '../../utils/theme';

const EditProfileScreen: React.FC = ({navigation}: any) => {
  const theme = useTheme();
  const {user, updateUser} = useAuthStore();
  const [formData, setFormData] = useState({
    full_name: user?.full_name || '',
    bio: user?.bio || '',
    avatar_url: user?.avatar_url || '',
  });
  const [isLoading, setIsLoading] = useState(false);
  const [isUploading, setIsUploading] = useState(false);

  const pickAvatar = () => {
    launchImageLibrary(
      {
        mediaType: 'photo',
        quality: 0.8,
      },
      async response => {
        if (response.assets && response.assets[0]) {
          setIsUploading(true);
          try {
            const result = await apiService.uploadMedia({
              uri: response.assets[0].uri,
              type: response.assets[0].type,
              name: response.assets[0].fileName || 'avatar.jpg',
            } as any);
            setFormData({...formData, avatar_url: result.media_url});
          } catch (error) {
            Alert.alert('Error', 'Failed to upload image');
          } finally {
            setIsUploading(false);
          }
        }
      },
    );
  };

  const handleSave = async () => {
    if (!formData.full_name) {
      Alert.alert('Error', 'Full name is required');
      return;
    }

    setIsLoading(true);
    try {
      const updatedUser = await apiService.updateProfile(formData);
      updateUser(updatedUser);
      Alert.alert('Success', 'Profile updated successfully', [
        {
          text: 'OK',
          onPress: () => navigation.goBack(),
        },
      ]);
    } catch (error) {
      Alert.alert('Error', 'Failed to update profile');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.scrollContent}>
      <Card style={styles.card} mode="elevated">
        <Card.Content style={styles.avatarSection}>
          <TouchableOpacity onPress={pickAvatar} disabled={isUploading}>
            <Avatar.Image
              size={100}
              source={
                formData.avatar_url
                  ? {uri: formData.avatar_url}
                  : require('../../assets/default-avatar.png')
              }
            />
            {isUploading && (
              <View style={styles.uploadingOverlay}>
                <ActivityIndicator size="small" color="#ffffff" />
              </View>
            )}
          </TouchableOpacity>
          <Button
            mode="text"
            onPress={pickAvatar}
            disabled={isUploading}
            style={styles.changeAvatarButton}>
            Change Photo
          </Button>
        </Card.Content>
      </Card>

      <Card style={styles.card} mode="elevated">
        <Card.Content>
          <TextInput
            label="Full Name"
            value={formData.full_name}
            onChangeText={text => setFormData({...formData, full_name: text})}
            mode="outlined"
            style={styles.input}
          />

          <TextInput
            label="Bio"
            value={formData.bio}
            onChangeText={text => setFormData({...formData, bio: text})}
            mode="outlined"
            multiline
            numberOfLines={4}
            style={styles.input}
            placeholder="Tell us about yourself..."
          />

          <TextInput
            label="Username"
            value={user?.username || ''}
            mode="outlined"
            disabled
            style={styles.input}
            helperText="Username cannot be changed"
          />

          <TextInput
            label="Email"
            value={user?.email || ''}
            mode="outlined"
            disabled
            style={styles.input}
            helperText="Email cannot be changed"
          />
        </Card.Content>
      </Card>

      <Button
        mode="contained"
        onPress={handleSave}
        style={styles.saveButton}
        loading={isLoading}
        disabled={isLoading}>
        Save Changes
      </Button>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f9fafb',
  },
  scrollContent: {
    padding: spacing.md,
  },
  card: {
    marginBottom: spacing.md,
    borderRadius: borderRadius.lg,
  },
  avatarSection: {
    alignItems: 'center',
    paddingVertical: spacing.lg,
  },
  uploadingOverlay: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundColor: 'rgba(0,0,0,0.5)',
    borderRadius: 50,
    justifyContent: 'center',
    alignItems: 'center',
  },
  changeAvatarButton: {
    marginTop: spacing.md,
  },
  input: {
    marginBottom: spacing.md,
  },
  saveButton: {
    marginTop: spacing.md,
    paddingVertical: spacing.xs,
  },
});

export default EditProfileScreen;
