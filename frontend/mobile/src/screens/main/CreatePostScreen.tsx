import React, {useState} from 'react';
import {
  View,
  StyleSheet,
  ScrollView,
  Image,
  TouchableOpacity,
  Alert,
} from 'react-native';
import {
  TextInput,
  Button,
  Text,
  useTheme,
  IconButton,
  ActivityIndicator,
} from 'react-native-paper';
import {launchImageLibrary} from 'react-native-image-picker';
import {apiService} from '../../services/api';
import {spacing, borderRadius} from '../../utils/theme';

const CreatePostScreen: React.FC = ({navigation}: any) => {
  const theme = useTheme();
  const [caption, setCaption] = useState('');
  const [mediaUrls, setMediaUrls] = useState<string[]>([]);
  const [isUploading, setIsUploading] = useState(false);
  const [isPosting, setIsPosting] = useState(false);

  const pickImage = () => {
    launchImageLibrary(
      {
        mediaType: 'photo',
        quality: 0.8,
        selectionLimit: 5,
      },
      async response => {
        if (response.assets && response.assets.length > 0) {
          setIsUploading(true);
          try {
            const uploadPromises = response.assets.map(asset =>
              apiService.uploadMedia({
                uri: asset.uri,
                type: asset.type,
                name: asset.fileName || 'image.jpg',
              } as any),
            );
            const results = await Promise.all(uploadPromises);
            const urls = results.map(r => r.media_url);
            setMediaUrls([...mediaUrls, ...urls]);
          } catch (error) {
            Alert.alert('Error', 'Failed to upload image');
          } finally {
            setIsUploading(false);
          }
        }
      },
    );
  };

  const removeImage = (index: number) => {
    setMediaUrls(mediaUrls.filter((_, i) => i !== index));
  };

  const handlePost = async () => {
    if (!caption && mediaUrls.length === 0) {
      Alert.alert('Error', 'Please add a caption or image');
      return;
    }

    setIsPosting(true);
    try {
      await apiService.createPost({
        caption: caption || undefined,
        media_urls: mediaUrls,
        product_tags: [], // TODO: Add product tagging
      });
      Alert.alert('Success', 'Post created successfully!', [
        {
          text: 'OK',
          onPress: () => {
            setCaption('');
            setMediaUrls([]);
            navigation.goBack();
          },
        },
      ]);
    } catch (error) {
      Alert.alert('Error', 'Failed to create post');
    } finally {
      setIsPosting(false);
    }
  };

  return (
    <View style={styles.container}>
      <ScrollView contentContainerStyle={styles.scrollContent}>
        <TextInput
          label="What's on your mind?"
          value={caption}
          onChangeText={setCaption}
          mode="outlined"
          multiline
          numberOfLines={6}
          style={styles.captionInput}
          placeholder="Write a caption..."
        />

        <View style={styles.mediaContainer}>
          {mediaUrls.map((url, index) => (
            <View key={index} style={styles.imageWrapper}>
              <Image source={{uri: url}} style={styles.image} />
              <IconButton
                icon="close-circle"
                size={24}
                style={styles.removeButton}
                onPress={() => removeImage(index)}
              />
            </View>
          ))}

          {isUploading ? (
            <View style={styles.uploadingContainer}>
              <ActivityIndicator size="large" color={theme.colors.primary} />
              <Text>Uploading...</Text>
            </View>
          ) : (
            <TouchableOpacity
              style={styles.addMediaButton}
              onPress={pickImage}>
              <IconButton icon="camera" size={40} />
              <Text variant="bodyMedium">Add Photo/Video</Text>
            </TouchableOpacity>
          )}
        </View>

        <Button
          mode="contained"
          onPress={handlePost}
          style={styles.postButton}
          loading={isPosting}
          disabled={isPosting}>
          Post
        </Button>
      </ScrollView>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#ffffff',
  },
  scrollContent: {
    padding: spacing.md,
  },
  captionInput: {
    marginBottom: spacing.md,
  },
  mediaContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    marginBottom: spacing.lg,
  },
  imageWrapper: {
    position: 'relative',
    margin: spacing.xs,
  },
  image: {
    width: 100,
    height: 100,
    borderRadius: borderRadius.md,
  },
  removeButton: {
    position: 'absolute',
    top: -10,
    right: -10,
    backgroundColor: '#ffffff',
  },
  uploadingContainer: {
    alignItems: 'center',
    justifyContent: 'center',
    padding: spacing.lg,
  },
  addMediaButton: {
    width: 100,
    height: 100,
    borderWidth: 2,
    borderColor: '#e5e7eb',
    borderStyle: 'dashed',
    borderRadius: borderRadius.md,
    alignItems: 'center',
    justifyContent: 'center',
    margin: spacing.xs,
  },
  postButton: {
    marginTop: spacing.md,
    paddingVertical: spacing.xs,
  },
});

export default CreatePostScreen;
